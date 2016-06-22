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

import ply.lex as lex


class LexException(Exception):
    def __init__(self, message, position):
        super(LexException, self).__init__(message)
        self.position = position


class Lexer(object):
    """
    Lexer for the PuppetDB query language.
    """
    def __init__(self, **kwargs):
        super(Lexer, self).__init__()
        self.lexer = lex.lex(object=self, **kwargs)

    def input(self, s):
        self.lexer.input(s)

    def token(self):
        return self.lexer.token()

    def __iter__(self):
        return self

    def next(self):
        t = self.token()
        if t is None:
            raise StopIteration()
        return t

    __next__ = next

    # List of token names.
    tokens = (
        'LPAREN',
        'RPAREN',
        'LBRACK',
        'RBRACK',
        'LBRACE',
        'RBRACE',
        'EQUALS',
        'NOTEQUALS',
        'MATCH',
        'NOTMATCH',
        'LESSTHANEQ',
        'LESSTHAN',
        'GREATERTHANEQ',
        'GREATERTHAN',
        'ASTERISK',
        'HASH',
        'DOT',
        'NOT',
        'AND',
        'OR',
        'BOOLEAN',
        'NUMBER',
        'STRING',
        'EXPORTED',
        'AT',
    )

    # Regular expression rules for simple tokens
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACK = r'\['
    t_RBRACK = r'\]'
    t_LBRACE = r'{'
    t_RBRACE = r'}'
    t_EQUALS = r'='
    t_NOTEQUALS = r'!='
    t_MATCH = r'~'
    t_NOTMATCH = r'!~'
    t_LESSTHANEQ = r'<='
    t_LESSTHAN = r'<'
    t_GREATERTHANEQ = r'>='
    t_GREATERTHAN = r'>'
    t_ASTERISK = r'\*'
    t_HASH = r'[#]'
    t_DOT = r'\.'
    t_EXPORTED = r'@@'
    t_AT = r'@'

    # Keywords
    def t_keyword(self, t):
        r'not|and|or'
        # Tokens defined by fuctions are added before regular expression tokens
        # so we must define a function to handle our keywords else they will be
        # lexed as bareword strings. The type here is just the uppercase
        # version of the token value.
        t.type = t.value.upper()
        return t

    # Boolean values
    def t_BOOLEAN(self, t):
        r'true|false'
        t.value = (t.value == 'true')
        return t

    # Numeric values
    def t_NUMBER(self, t):
        r'-?\d+'
        t.value = int(t.value)
        return t

    # The next three functions handle string parsing, because there are three
    # slightly different syntaxes for strings (which are handled the same way
    # in the parser).
    def t_STRING_bareword(self, t):
        r'[-\w_:]+'
        t.type = 'STRING'
        # This is a bareword string, it has no quotes around it so the value is
        # unchanged.
        return t

    def t_STRING_double_quoted(self, t):
        r'"(\\.|[^\\"])*"'
        t.type = 'STRING'
        # This is a double-quoted string. The regex handles most of what we
        # need but we must strip off the quote characters around the string.
        t.value = t.value[1:-1]
        return t

    def t_STRING_single_quoted(self, t):
        r"'(\\.|[^\\'])*'"
        t.type = 'STRING'
        # This is a single-quoted string. The regex handles most of what we
        # need but we must strip off the quote characters around the string.
        t.value = t.value[1:-1]
        return t

    # A string containing ignored characters
    t_ignore = " \t\n\r\f\v"  # all whitespace

    # Error handling rule
    def t_error(self, t):
        msg = "Illegal character '{0}'".format(t.value[0])
        raise LexException(msg, t.lexpos)
