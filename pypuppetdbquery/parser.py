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

import ply.yacc as yacc

from . import ast
from .lexer import Lexer


class ParseException(Exception):
    def __init__(self, message, position):
        super(ParseException, self).__init__(message)
        self.position = position


class Parser(object):
    """
    Parser for the PuppetDB query language.
    """
    def __init__(self, lex_options=None, yacc_options=None):
        super(Parser, self).__init__()

        lex_options = lex_options or {}
        lex_options.setdefault('debug', False)
        lex_options.setdefault('optimize', True)

        self.lexer = Lexer(**lex_options)
        self.tokens = self.lexer.tokens

        yacc_options = yacc_options or {}
        yacc_options.setdefault('debug', False)
        yacc_options.setdefault('optimize', True)

        self.parser = yacc.yacc(module=self, **yacc_options)

    def parse(self, text, debug=0):
        return self.parser.parse(input=text, lexer=self.lexer, debug=debug)

    start = 'query'

    def p_query(self, p):
        """
        query : expr
              | empty
        """
        p[0] = ast.Query(p[1])

    def p_expr_identifier_path(self, p):
        'expr : identifier_path'
        p[0] = ast.RegexNodeMatch(p[1])

    def p_expr_not(self, p):
        'expr : NOT expr'
        p[0] = ast.NotExpression(p[2])

    def p_expr_and(self, p):
        'expr : expr AND expr'
        p[0] = ast.AndExpression(p[1], p[3])

    def p_expr_or(self, p):
        'expr : expr OR expr'
        p[0] = ast.OrExpression(p[1], p[3])

    def p_expr_parenthesized(self, p):
        'expr : LPAREN expr RPAREN'
        p[0] = ast.ParenthesizedExpression(p[2])

    def p_expr(self, p):
        """
        expr : resource_expr
             | comparison_expr
             | subquery
        """
        p[0] = p[1]

    def p_literal(self, p):
        """
        literal : boolean
                | string
                | integer
                | float
        """
        p[0] = ast.Literal(p[1])

    def p_literal_date(self, p):
        'literal : AT string'
        p[0] = ast.Date(p[1])

    def p_comparison_op(self, p):
        """
        comparison_op : MATCH
                      | NOTMATCH
                      | EQUALS
                      | NOTEQUALS
                      | GREATERTHAN
                      | GREATERTHANEQ
                      | LESSTHAN
                      | LESSTHANEQ
        """
        p[0] = p[1]

    def p_comparison_expr(self, p):
        'comparison_expr : identifier_path comparison_op literal'
        p[0] = ast.Comparison(p[2], p[1], p[3])

    def p_identifier(self, p):
        """
        identifier : string
                   | integer
        """
        p[0] = ast.Identifier(p[1])

    def p_identifier_regexp(self, p):
        'identifier : MATCH string'
        p[0] = ast.RegexpIdentifier(p[2])

    def p_identifier_wild(self, p):
        'identifier : ASTERISK'
        p[0] = ast.RegexpIdentifier(r'.*')

    def p_identifier_path(self, p):
        'identifier_path : identifier'
        p[0] = ast.IdentifierPath(p[1])

    def p_identifier_path_nested(self, p):
        'identifier_path : identifier_path DOT identifier'
        p[0] = p[1].components.append(p[3])

    def p_subquery_comparison(self, p):
        'subquery : HASH string DOT comparison_expr'
        p[0] = ast.Subquery(p[2], p[4])

    def p_subquery_block(self, p):
        'subquery : HASH string block_expr'
        p[0] = ast.Subquery(p[2], p[3])

    def p_block_expr(self, p):
        'block_expr : LBRACE expr RBRACE'
        p[0] = ast.BlockExpression(p[2])

    def p_resource_expr(self, p):
        'resource_expr : string LBRACK identifier RBRACK'
        p[0] = ast.Resource(p[1], p[3], False)

    def p_resource_expr_param(self, p):
        'resource_expr : string LBRACK identifier RBRACK block_expr'
        p[0] = ast.Resource(p[1], p[3], False, p[5])

    def p_resource_expr_expored(self, p):
        'resource_expr : EXPORTED string LBRACK identifier RBRACK'
        p[0] = ast.Resource(p[2], p[4], True)

    def p_resource_expr_expored_param(self, p):
        'resource_expr : EXPORTED string LBRACK identifier RBRACK block_expr'
        p[0] = ast.Resource(p[2], p[4], True, p[6])

    def p_boolean(self, p):
        'boolean : BOOLEAN'
        p[0] = p[1]

    def p_integer(self, p):
        'integer : NUMBER'
        p[0] = p[1]

    def p_string(self, p):
        'string  : STRING'
        p[0] = p[1]

    def p_float(self, p):
        'float : NUMBER DOT NUMBER'
        p[0] = float(p[1] + '.' + p[3])

    def p_empty(self, p):
        'empty :'
        pass

    precedence = (
        ('right', 'NOT'),
        ('left', 'EQUALS', 'MATCH', 'LESSTHAN', 'GREATERTHAN'),
        ('left', 'AND'),
        ('left', 'OR'),
    )

    def p_error(self, p):
        if p:
            raise ParseException("before: {}".format(p.value), p.lexpos)
        else:
            raise ParseException('at end of input', None)
