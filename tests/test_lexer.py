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

from pypuppetdbquery.lexer import Lexer, LexException


class TestLexer(unittest.TestCase):
    """
    Test cases for :class:`pypuppetdbquery.lexer.Lexer`.
    """
    def setUp(self):
        self.lexer = Lexer(
            debug=False,
            optimize=False,
        )

    def _lex(self, s):
        self.lexer.input(s)
        return list(self.lexer)

    def test_empty_queries(self):
        out = self._lex('')
        self.assertEqual(out, [])

    def test_all_tokens(self):
        # The string below must contain all possible lexer tokens
        out = self._lex(
            "(not)[and]{or}=true!=false~0!~1.024<=<>=>*#.@@foo@'bar'\"baz\"")

        # Expected result of lexing the above string
        expect = [
            ('LPAREN', '(', 1, 0),
            ('NOT', 'not', 1, 1),
            ('RPAREN', ')', 1, 4),
            ('LBRACK', '[', 1, 5),
            ('AND', 'and', 1, 6),
            ('RBRACK', ']', 1, 9),
            ('LBRACE', '{', 1, 10),
            ('OR', 'or', 1, 11),
            ('RBRACE', '}', 1, 13),
            ('EQUALS', '=', 1, 14),
            ('BOOLEAN', True, 1, 15),
            ('NOTEQUALS', '!=', 1, 19),
            ('BOOLEAN', False, 1, 21),
            ('MATCH', '~', 1, 26),
            ('NUMBER', 0, 1, 27),
            ('NOTMATCH', '!~', 1, 28),
            ('FLOAT', 1.024, 1, 30),
            ('LESSTHANEQ', '<=', 1, 35),
            ('LESSTHAN', '<', 1, 37),
            ('GREATERTHANEQ', '>=', 1, 38),
            ('GREATERTHAN', '>', 1, 40),
            ('ASTERISK', '*', 1, 41),
            ('HASH', '#', 1, 42),
            ('DOT', '.', 1, 43),
            ('EXPORTED', '@@', 1, 44),
            ('STRING', 'foo', 1, 46),
            ('AT', '@', 1, 49),
            ('STRING', 'bar', 1, 50),
            ('STRING', 'baz', 1, 55),
        ]

        # Ensure that every token in the lexer token list is included in the
        # expectation list above.
        self.assertEqual(
            frozenset(x[0] for x in expect),
            frozenset(x.type for x in out))

        # Now check that the lexer's output matches our expectation list
        for i, j in zip(out, expect):
            self.assertEqual((i.type, i.value, i.lineno, i.lexpos), j)

    def test_invalid_input(self):
        def _should_raise():
            self._lex('$')
        self.assertRaises(LexException, _should_raise)
