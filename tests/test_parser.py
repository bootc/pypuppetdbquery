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

import unittest

from pypuppetdbquery import ast
from pypuppetdbquery.parser import Parser, ParseException


class TestParster(unittest.TestCase):
    """
    Test cases for :class:`pypuppetdbquery.parser.Parser`.
    """
    def setUp(self):
        self.parser = Parser(
            lex_options={
                'debug': False,
                'optimize': False,
            },
            yacc_options={
                'debug': False,
                'optimize': False,
                'write_tables': False,
            },
        )

    def _parse(self, s):
        return self.parser.parse(s)

    def test_empty_queries(self):
        out = self._parse('')
        self.assertTrue(isinstance(out, ast.Query))
        self.assertTrue(out.expression is None)

    def test_double_quoted_strings(self):
        out = self._parse('foo="bar"')
        expect = ast.Query(
            ast.Comparison(
                '=',
                ast.IdentifierPath([
                    ast.Identifier('foo'),
                ]),
                ast.Literal('bar')))
        self.assertEqual(repr(out), repr(expect))

    def test_logical_operators(self):
        out = self._parse('foo=1 or (bar=2 and baz=3)')
        expect = ast.Query(
            ast.OrExpression(
                ast.Comparison(
                    '=',
                    ast.IdentifierPath([ast.Identifier('foo')]),
                    ast.Literal(1)),
                ast.ParenthesizedExpression(
                    ast.AndExpression(
                        ast.Comparison(
                            '=',
                            ast.IdentifierPath([ast.Identifier('bar')]),
                            ast.Literal(2)),
                        ast.Comparison(
                            '=',
                            ast.IdentifierPath([ast.Identifier('baz')]),
                            ast.Literal(3))))))
        self.assertEqual(repr(out), repr(expect))

    def test_resource_queries_for_exported_resources(self):
        out = self._parse('@@file[foo]')
        expect = ast.Query(
            ast.Resource('file', ast.Identifier('foo'), True, None))
        self.assertEqual(repr(out), repr(expect))

    def test_resource_queries_for_exported_resources_with_parameters(self):
        out = self._parse('@@file[foo]{bar=baz}')
        expect = ast.Query(
            ast.Resource(
                'file',
                ast.Identifier('foo'),
                True,
                ast.BlockExpression(
                    ast.Comparison(
                        '=',
                        ast.IdentifierPath([ast.Identifier('bar')]),
                        ast.Literal('baz')))))
        self.assertEqual(repr(out), repr(expect))

    def test_resource_queries_with_type_and_regexp_identifier(self):
        out = self._parse('class[~foo]')
        expect = ast.Query(
            ast.Resource('class', ast.RegexpIdentifier('foo'), False, None))
        self.assertEqual(repr(out), repr(expect))

    def test_resource_queries_with_type_title_and_parameters(self):
        out = self._parse('file[foo]{bar=baz}')
        expect = ast.Query(
            ast.Resource(
                'file',
                ast.Identifier('foo'),
                False,
                ast.BlockExpression(
                    ast.Comparison(
                        '=',
                        ast.IdentifierPath([ast.Identifier('bar')]),
                        ast.Literal('baz')))))
        self.assertEqual(repr(out), repr(expect))

    def test_negate_expression(self):
        out = self._parse('not foo=bar')
        expect = ast.Query(
            ast.NotExpression(
                ast.Comparison(
                    '=',
                    ast.IdentifierPath([ast.Identifier('foo')]),
                    ast.Literal('bar'))))
        self.assertEqual(repr(out), repr(expect))

    def test_single_string_expressions(self):
        out = self._parse('foo.bar.com')
        expect = ast.Query(
            ast.RegexpNodeMatch(
                ast.IdentifierPath([
                    ast.Identifier('foo'),
                    ast.Identifier('bar'),
                    ast.Identifier('com')])))
        self.assertEqual(repr(out), repr(expect))

    def test_structured_facts_with_wildcard_operator(self):
        out = self._parse('foo.bar.*=baz')
        expect = ast.Query(
            ast.Comparison(
                '=',
                ast.IdentifierPath([
                    ast.Identifier('foo'),
                    ast.Identifier('bar'),
                    ast.RegexpIdentifier('.*')]),
                ast.Literal('baz')))
        self.assertEqual(repr(out), repr(expect))

    def test_node_subqueries(self):
        out = self._parse('#node.catalog_environment=production')
        expect = ast.Query(
            ast.Subquery(
                'node',
                ast.Comparison(
                    '=',
                    ast.IdentifierPath([
                        ast.Identifier('catalog_environment')]),
                    ast.Literal('production'))))
        self.assertEqual(repr(out), repr(expect))

    def test_node_subqueries_with_block_of_conditions(self):
        out = self._parse('#node { catalog_environment=production }')
        expect = ast.Query(
            ast.Subquery(
                'node',
                ast.BlockExpression(
                    ast.Comparison(
                        '=',
                        ast.IdentifierPath([
                            ast.Identifier('catalog_environment')]),
                        ast.Literal('production')))))
        self.assertEqual(repr(out), repr(expect))

    def test_dates_in_queries(self):
        out = self._parse('#node.report_timestamp<@"Sep 9, 2014"')
        expect = ast.Query(
            ast.Subquery(
                'node',
                ast.Comparison(
                    '<',
                    ast.IdentifierPath([ast.Identifier('report_timestamp')]),
                    ast.Date('Sep 9, 2014'))))
        self.assertEqual(repr(out), repr(expect))

    def test_boolean_values(self):
        out = self._parse('foo=true')
        expect = ast.Query(
            ast.Comparison(
                '=',
                ast.IdentifierPath([ast.Identifier('foo')]),
                ast.Literal(True)))
        self.assertEqual(repr(out), repr(expect))

    def test_float_values(self):
        out = self._parse('foo=1.024')
        expect = ast.Query(
            ast.Comparison(
                '=',
                ast.IdentifierPath([ast.Identifier('foo')]),
                ast.Literal(1.024)))
        self.assertEqual(repr(out), repr(expect))

    def test_invalid_input(self):
        def _should_raise():
            self._parse('}')
        self.assertRaises(ParseException, _should_raise)

    def test_invalid_input_eof(self):
        def _should_raise():
            self._parse('foo=')
        self.assertRaises(ParseException, _should_raise)
