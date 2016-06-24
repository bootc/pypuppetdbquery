# -*- coding: utf-8 -*-
#
# This file is part of pypuppetdbquery.
# Copyright © 2016  Chris Boot <bootc@bootc.net>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import dateutil.parser
import re

from . import ast


class Evaluator(object):
    """
    Converts a :mod:`pypuppetdbquery.ast` Abstract Syntax Tree into a PuppetDB
    native AST query.
    """

    #: Regular expression used when converting CamelCase class names to
    #: underscore_separated names.
    DECAMEL_RE = re.compile(r'(?!^)([A-Z]+)')

    def evaluate(self, ast, mode='nodes'):
        """
        Process a parsed PuppetDBQuery AST and return a PuppetDB AST.

        The resulting PuppetDB AST is a native Python list. It will need
        converting to JSON (using :func:`json.dumps`) before it can be used
        with PuppetDB.

        :param pypuppetdbquery.ast.Query ast: Root of the AST to evaulate
        :param str mode: PuppetDB endpoint to target
        :return: PuppetDB AST
        :rtype: list
        """
        return self._visit(ast, [mode])

    def _subquery(self, from_mode, to_mode, query):
        if from_mode == 'none':
            return query

        return ['in', 'certname', [
            'extract', 'certname', [
                "select_{0}".format(to_mode), query]]]

    def _comparison(self, operator, left, right):
        if operator[0] == '!':
            return ['not', [operator[1], left, right]]
        else:
            return [operator, left, right]

    def _capitalize_class(self, name):
        return '::'.join([x.capitalize() for x in name.split('::')])

    def _visit(self, node, path):
        if isinstance(node, list):
            return [self._visit(x, path) for x in node]

        # Convert CamelCase node class name to underscores
        klass = node.__class__.__name__
        underscore = self.DECAMEL_RE.sub(r'_\1', klass).lower()

        visitor = getattr(self, '_visit_{0}'.format(underscore))
        return visitor(node, path)

    def _visit_literal(self, node, path):
        return node.value

    def _visit_date(self, node, path):
        return dateutil.parser.parse(node.value).strftime('%Y-%m-%dT%H:%M:%SZ')

    def _visit_query(self, node, path):
        if node.expression is None:
            return None
        else:
            return self._visit(node.expression, path)

    def _visit_and_expression(self, node, path):
        return ['and',
                self._visit(node.left, path),
                self._visit(node.right, path)]

    def _visit_or_expression(self, node, path):
        return ['or',
                self._visit(node.left, path),
                self._visit(node.right, path)]

    def _visit_not_expression(self, node, path):
        return ['not', self._visit(node.expression, path)]

    def _visit_parenthesized_expression(self, node, path):
        return self._visit(node.expression, path)

    def _visit_block_expression(self, node, path):
        return self._visit(node.expression, path)

    def _visit_comparison(self, node, path):
        left = self._visit(node.left, path)
        right = self._visit(node.right, path)

        if path[-1] == 'subquery':
            if len(left) == 1:
                left = left[0]
            return self._comparison(node.operator, left, right)
        elif path[-1] == 'resources':
            if left[0] == 'tag':
                return self._comparison(
                    node.operator, left[0], right)
            else:
                return self._comparison(
                    node.operator, ['parameter', left[0]], right)
        else:
            return self._subquery(
                path[-1], 'fact_contents',
                ['and', left, self._comparison(node.operator, 'value', right)])

    def _visit_identifier(self, node, path):
        if path[-1] == 'regexp':
            return re.escape(node.name)
        else:
            return node.name

    def _visit_regexp_identifier(self, node, path):
        return node.name

    def _visit_identifier_path(self, node, path):
        if path[-1] in ['subquery', 'resources']:
            return self._visit(node.components, path)
        elif path[-1] == 'regexp':
            return '.'.join(self._visit(node.components, path))
        else:
            # Check if any of the children are of regexp type in that case we
            # need to escape the others and use the ~> operator
            if any(isinstance(x, ast.RegexpIdentifier)
                   for x in node.components):
                path.append('regexp')
                ret = ['~>', 'path', self._visit(node.components, path)]
                path.pop()
                return ret
            else:
                return ['=', 'path', self._visit(node.components, path)]

    def _visit_subquery(self, node, path):
        path.append('subquery')
        ret = self._subquery(path[-2], node.endpoint + 's',
                             self._visit(node.expression, path))
        path.pop()
        return ret

    def _visit_resource(self, node, path):
        path.append('resources')

        regexp = isinstance(node.title, ast.RegexpIdentifier)
        if not regexp and node.res_type.lower() == 'class':
            title = self._capitalize_class(self._visit(node.title, path))
        else:
            title = self._visit(node.title, path)

        res_type = self._capitalize_class(node.res_type)
        query = [
            'and',
            ['=', 'type', res_type],
            ['~' if regexp else '=', 'title', title],
            ['=', 'exported', node.exported],
        ]

        if node.parameters:
            query.append(self._visit(node.parameters, path))

        path.pop()

        return self._subquery(path[-1], 'resources', query)

    def _visit_regexp_node_match(self, node, path):
        path.append('regexp')
        ret = ['~', 'certname', re.escape(self._visit(node.value, path))]
        path.pop()
        return ret
