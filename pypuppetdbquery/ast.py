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
"""
Abstract Syntax Tree (AST) for the PuppetDBQuery language. These simple classes
are used by the :class:`pypuppetdbquery.parser.Parser` in order to represent
the parsed syntax tree.
"""

import inspect


class Node(object):
    def __repr__(self):
        # Represent the variables defined in the constructor in the same order
        # that they are listed in the constructor.
        members = []
        for var in inspect.getargspec(self.__init__).args:
            if var == 'self':
                continue

            members.append(repr(getattr(self, var)))

        # Put it together with the class name
        return "{cls}({members})".format(
            cls=self.__class__.__name__, members=', '.join(members))


class Literal(Node):
    def __init__(self, value):
        self.value = value


class Date(Literal):
    pass


class Query(Node):
    def __init__(self, expression):
        self.expression = expression


class Expression(Node):
    pass


class UnaryExpression(Node):
    def __init__(self, expression):
        self.expression = expression


class BinaryExpression(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class AndExpression(BinaryExpression):
    pass


class OrExpression(BinaryExpression):
    pass


class NotExpression(UnaryExpression):
    pass


class ParenthesizedExpression(UnaryExpression):
    pass


class BlockExpression(UnaryExpression):
    pass


class Comparison(Expression):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right


class Identifier(Node):
    def __init__(self, name):
        self.name = name


class RegexpIdentifier(Identifier):
    pass


class IdentifierPath(Node):
    def __init__(self, components):
        self.components = components


class Subquery(Node):
    def __init__(self, endpoint, expression):
        self.endpoint = endpoint
        self.expression = expression


class Resource(Expression):
    def __init__(self, res_type, title, exported, parameters=None):
        self.res_type = res_type
        self.title = title
        self.exported = exported
        self.parameters = parameters


class RegexpNodeMatch(Expression):
    def __init__(self, value):
        self.value = value
