# -*- coding: utf-8 -*-
#
# This file is part of pypuppetdbquery.
# Copyright © 2016  Chris Boot <bootc@bootc.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


class Node(object):
    pass


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
    def __init__(self, component):
        self.components = [component]


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
