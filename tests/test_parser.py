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

from pypuppetdbquery.evaluator import Evaluator
from pypuppetdbquery.parser import Parser
from util import CompatTestCase


class TestParser(CompatTestCase):
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
        self.evaluator = Evaluator()

    def _parse(self, s, *args):
        ast = self.parser.parse(s)
        return self.evaluator.evaluate(ast, *args)

    def test_empty_queries(self):
        out = self._parse('')
        self.assertIsNone(out)

    def test_double_quoted_strings(self):
        out = self._parse('foo="bar"')
        self.assertEquals(out, [
            'in', 'certname',
            ['extract', 'certname',
             ['select_fact_contents',
              ['and',
               ['=', 'path', ['foo']],
               ['=', 'value', 'bar']]]]])

    def test_single_quoted_strings(self):
        out = self._parse("foo='bar'")
        self.assertEquals(out, [
            'in', 'certname',
            ['extract', 'certname',
             ['select_fact_contents',
              ['and',
               ['=', 'path', ['foo']],
               ['=', 'value', 'bar']]]]])

    def test_equals_operator(self):
        out = self._parse('foo=bar')
        self.assertEqual(out, [
            'in', 'certname',
            ['extract', 'certname',
             ['select_fact_contents',
              ['and',
               ['=', 'path', ['foo']],
               ['=', 'value', 'bar']]]]])

    def test_not_equals_operator(self):
        out = self._parse('foo!=bar')
        self.assertEquals(out, [
            'in', 'certname',
            ['extract', 'certname',
             ['select_fact_contents',
              ['and',
               ['=', 'path', ['foo']],
               ['not', ['=', 'value', 'bar']]]]]])

    def test_match_operator(self):
        out = self._parse('foo~bar')
        self.assertEquals(out, [
            'in', 'certname',
            ['extract', 'certname',
             ['select_fact_contents',
              ['and',
               ['=', 'path', ['foo']],
               ['~', 'value', 'bar']]]]])

    def test_not_match_operator(self):
        out = self._parse('foo!~bar')
        self.assertEquals(out, [
            'in', 'certname',
            ['extract', 'certname',
             ['select_fact_contents',
              ['and',
               ['=', 'path', ['foo']],
               ['not', ['~', 'value', 'bar']]]]]])

    def test_greater_than_eq_operator(self):
        out = self._parse('foo>=1')
        self.assertEquals(out, [
            'in', 'certname',
            ['extract', 'certname',
             ['select_fact_contents',
              ['and',
               ['=', 'path', ['foo']],
               ['>=', 'value', 1]]]]])

    def test_less_than_eq_operator(self):
        out = self._parse('foo<=1')
        self.assertEquals(out, [
            'in', 'certname',
            ['extract', 'certname',
             ['select_fact_contents',
              ['and',
               ['=', 'path', ['foo']],
               ['<=', 'value', 1]]]]])

    def test_greater_than_operator(self):
        out = self._parse('foo>1')
        self.assertEquals(out, [
            'in', 'certname',
            ['extract', 'certname',
             ['select_fact_contents',
              ['and',
               ['=', 'path', ['foo']],
               ['>', 'value', 1]]]]])

    def test_less_than_operator(self):
        out = self._parse('foo<1')
        self.assertEquals(out, [
            'in', 'certname',
            ['extract', 'certname',
             ['select_fact_contents',
              ['and',
               ['=', 'path', ['foo']],
               ['<', 'value', 1]]]]])

    def test_precedence_a(self):
        out = self._parse('foo=1 or bar=2 and baz=3')
        self.assertEquals(out, [
            'or',
            ['in', 'certname',
             ['extract', 'certname',
              ['select_fact_contents',
               ['and', ['=', 'path', ['foo']], ['=', 'value', 1]]]]],
            ['and',
             ['in', 'certname',
              ['extract', 'certname',
               ['select_fact_contents',
                ['and', ['=', 'path', ['bar']], ['=', 'value', 2]]]]],
             ['in', 'certname',
              ['extract', 'certname',
               ['select_fact_contents',
                ['and',
                 ['=', 'path', ['baz']],
                 ['=', 'value', 3]]]]]]])

    def test_precedence_b(self):
        out = self._parse('(foo=1 or bar=2) and baz=3')
        self.assertEquals(out, [
            'and',
            ['or',
             ['in', 'certname',
              ['extract', 'certname',
               ['select_fact_contents',
                ['and', ['=', 'path', ['foo']], ['=', 'value', 1]]]]],
             ['in', 'certname',
              ['extract', 'certname',
               ['select_fact_contents',
                ['and',
                 ['=', 'path', ['bar']],
                 ['=', 'value', 2]]]]]],
            ['in', 'certname',
             ['extract', 'certname',
              ['select_fact_contents',
               ['and', ['=', 'path', ['baz']], ['=', 'value', 3]]]]]])

    def test_resource_queries_for_exported_resources(self):
        out = self._parse('@@file[foo]')
        self.assertEquals(out, [
            'in', 'certname',
            ['extract', 'certname',
             ['select_resources',
              ['and',
               ['=', 'type', 'File'],
               ['=', 'title', 'foo'],
               ['=', 'exported', True]]]]])

    def test_resource_queries_with_type_and_title(self):
        out = self._parse('file[foo]')
        self.assertEquals(out, [
            "in", "certname",
            ["extract", "certname",
             ["select_resources",
              ["and",
               ["=", "type", "File"],
               ["=", "title", "foo"],
               ["=", "exported", False]]]]])

    def test_resource_queries_with_type_title_and_parameters(self):
        out = self._parse('file[foo]{bar=baz}')
        self.assertEquals(out, [
            'in', 'certname',
            ['extract', 'certname',
             ['select_resources',
              ['and',
               ['=', 'type', 'File'],
               ['=', 'title', 'foo'],
               ['=', 'exported', False],
               ['=', ['parameter', 'bar'], 'baz']]]]])

    def test_resource_queries_with_tags(self):
        out = self._parse('file[foo]{tag=baz}')
        self.assertEquals(out, [
            'in', 'certname',
            ['extract', 'certname',
             ['select_resources',
              ['and',
               ['=', 'type', 'File'],
               ['=', 'title', 'foo'],
               ['=', 'exported', False],
               ['=', 'tag', 'baz']]]]])

    def test_precedence_within_resource_parameter_queries_a(self):
        out = self._parse('file[foo]{foo=1 or bar=2 and baz=3}')
        self.assertEquals(out, [
            'in', 'certname',
            ['extract', 'certname',
             ['select_resources',
              ['and',
               ['=', 'type', 'File'],
               ['=', 'title', 'foo'],
               ['=', 'exported', False],
               ['or',
                ['=', ['parameter', 'foo'], 1],
                ['and',
                 ['=', ['parameter', 'bar'], 2],
                 ['=', ['parameter', 'baz'], 3]]]]]]])

    def test_precedence_within_resource_parameter_queries_b(self):
        out = self._parse('file[foo]{(foo=1 or bar=2) and baz=3}')
        self.assertEquals(out, [
            'in', 'certname',
            ['extract', 'certname',
             ['select_resources',
              ['and',
               ['=', 'type', 'File'],
               ['=', 'title', 'foo'],
               ['=', 'exported', False],
               ['and',
                ['or',
                 ['=', ['parameter', 'foo'], 1],
                 ['=', ['parameter', 'bar'], 2]],
                ['=', ['parameter', 'baz'], 3]]]]]])

    def test_capitalize_class_names(self):
        out = self._parse('class[foo::bar]')
        self.assertEquals(out, [
            'in', 'certname',
            ['extract', 'certname',
             ['select_resources',
              ['and',
               ['=', 'type', 'Class'],
               ['=', 'title', 'Foo::Bar'],
               ['=', 'exported', False]]]]])

    def test_resource_queries_with_regexp_title_matching(self):
        out = self._parse('class[~foo]')
        self.assertEquals(out, [
            'in', 'certname',
            ['extract', 'certname',
             ['select_resources',
              ['and',
               ['=', 'type', 'Class'],
               ['~', 'title', 'foo'],
               ['=', 'exported', False]]]]])

    def test_negate_expressions(self):
        out = self._parse('not foo=bar')
        self.assertEquals(out, [
            'not',
            ['in', 'certname',
             ['extract', 'certname',
              ['select_fact_contents',
               ['and',
                ['=', 'path', ['foo']],
                ['=', 'value', 'bar']]]]]])

    def test_single_string_expressions(self):
        out = self._parse('foo.bar.com')
        self.assertEquals(out, [
            '~', 'certname', 'foo\\.bar\\.com'])

    def test_structured_facts(self):
        out = self._parse('foo.bar=baz')
        self.assertEquals(out, [
            'in', 'certname',
            ['extract', 'certname',
             ['select_fact_contents',
              ['and',
               ['=', 'path', ['foo', 'bar']],
               ['=', 'value', 'baz']]]]])

    def test_structured_facts_with_array_component(self):
        out = self._parse('foo.bar.0=baz')
        self.assertEqual(out, [
            'in', 'certname',
            ['extract', 'certname',
             ['select_fact_contents',
              ['and',
               ['=', 'path',
                ['foo', 'bar', 0]],
               ['=', 'value', 'baz']]]]])

    def test_structured_facts_with_match_operator(self):
        out = self._parse('foo.bar.~".*"=baz')
        self.assertEqual(out, [
            'in', 'certname',
            ['extract', 'certname',
             ['select_fact_contents',
              ['and',
               ['~>', 'path',
                ['foo', 'bar', '.*']],
               ['=', 'value', 'baz']]]]])

    def test_structured_facts_with_wildcard_operator(self):
        out = self._parse('foo.bar.*=baz')
        self.assertEqual(out, [
            'in', 'certname',
            ['extract', 'certname',
             ['select_fact_contents',
              ['and',
               ['~>', 'path',
                ['foo', 'bar', '.*']],
               ['=', 'value', 'baz']]]]])

    def test_node_subqueries(self):
        out = self._parse('#node.catalog_environment=production')
        self.assertEqual(out, [
            'in', 'certname',
            ['extract', 'certname',
             ['select_nodes',
              ['=', 'catalog_environment', 'production']]]])

    def test_node_subqueries_with_block_of_conditions(self):
        out = self._parse('#node { catalog_environment=production }')
        self.assertEqual(out, [
            'in', 'certname',
            ['extract', 'certname',
             ['select_nodes',
              ['=', 'catalog_environment', 'production']]]])

    def test_node_subqueries_with_fact_query(self):
        out = self._parse('#node.catalog_environment=production and foo=bar')
        self.assertEqual(out, [
            'and',
            ['in', 'certname',
             ['extract', 'certname',
              ['select_nodes',
               ['=', 'catalog_environment', 'production']]]],
            ['in', 'certname',
             ['extract', 'certname',
              ['select_fact_contents',
               ['and',
                ['=', 'path',
                 ['foo']],
                ['=', 'value', 'bar']]]]]])

    def test_node_subquery_fact_field(self):
        out = self._parse('#node.fact.bar=baz')
        self.assertEqual(out, [
            'in', 'certname',
            ['extract', 'certname',
             ['select_nodes',
              ['=',
               ['fact', 'bar'], 'baz']]]])

    def test_escape_non_match_parts_on_structured_facts_with_match_op(self):
        out = self._parse('"foo.bar".~".*"=baz')
        self.assertEqual(out, [
            'in', 'certname',
            ['extract', 'certname',
             ['select_fact_contents',
              ['and',
               ['~>', 'path',
                ['foo\\.bar', '.*']],
               ['=', 'value', 'baz']]]]])

    def test_dates_in_queries(self):
        out = self._parse('#node.report_timestamp<@"Sep 9, 2014"')
        self.assertEqual(out, [
            'in', 'certname',
            ['extract', 'certname',
             ['select_nodes',
              ['<', 'report_timestamp', '2014-09-09T00:00:00Z']]]])

    def test_does_not_wrap_subquery_with_mode_none(self):
        out = self._parse('class[apache]', 'none')
        self.assertEqual(out, [
            'and',
            ['=', 'type', 'Class'],
            ['=', 'title', 'Apache'],
            ['=', 'exported', False]])
