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

import unittest

from pypuppetdbquery import ast
from pypuppetdbquery.parser import Parser


class TestParser(unittest.TestCase):
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

    def test_empty_query(self):
        out = self.parser.parse('')
        self.assertIsInstance(out, ast.Query)
        self.assertIsNone(out.expression)

    def test_double_quoted_strings(self):
        out = self.parser.parse('foo="bar"')
        self.assertIsInstance(out, ast.Query)

        self.assertIsInstance(out.expression, ast.Comparison)
        self.assertEquals(out.expression.operator, '=')

        self.assertIsInstance(out.expression.left, ast.IdentifierPath)
        self.assertEquals(out.expression.left.flatten(), 'foo')

        self.assertIsInstance(out.expression.right, ast.Literal)
        self.assertEquals(out.expression.right.value, 'bar')
