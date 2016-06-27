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

import json
import mock
import unittest

from pypuppetdbquery import parse, query_facts, query_fact_contents


class _FakeNode(object):
    def __init__(self, node, name, value):
        self.node = node
        self.name = name
        self.value = value


class TestFrontendParse(unittest.TestCase):
    """
    Test cases targetting :func:`pypuppetdbquery.parse`.
    """

    def _parse(self, s, **kwargs):
        return parse(
            s,
            lex_options={
                'debug': False,
                'optimize': False,
            },
            yacc_options={
                'debug': False,
                'optimize': False,
                'write_tables': False,
            },
            **kwargs)

    def test_empty_queries(self):
        out = self._parse('')
        self.assertTrue(out is None)

    def test_simple_json(self):
        out = self._parse('foo=bar')
        expect = json.dumps([
            'in', 'certname',
            ['extract', 'certname',
             ['select_fact_contents',
              ['and',
               ['=', 'path', ['foo']],
               ['=', 'value', 'bar']]]]])
        self.assertEqual(out, expect)

    def test_simple_raw(self):
        out = self._parse('foo=bar', json=False)
        expect = [
            'in', 'certname',
            ['extract', 'certname',
             ['select_fact_contents',
              ['and',
               ['=', 'path', ['foo']],
               ['=', 'value', 'bar']]]]]
        self.assertEqual(out, expect)


class TestFrontendQueryFacts(unittest.TestCase):
    """
    Test cases targetting :func:`pypuppetdbquery.query_facts`.
    """

    def _query_facts(self, pdb, s, facts=None, raw=False):
        return query_facts(
            pdb, s, facts, raw,
            lex_options={
                'debug': False,
                'optimize': False,
            },
            yacc_options={
                'debug': False,
                'optimize': False,
                'write_tables': False,
            })

    def test_query_facts_with_query_and_facts_list(self):
        mock_pdb = mock.NonCallableMock()
        mock_pdb.facts = mock.Mock(return_value=[
            _FakeNode('alpha', 'foo', 'bar'),
        ])

        node_facts = self._query_facts(mock_pdb, 'foo=bar', ['foo'])

        mock_pdb.facts.assert_called_once_with(query=json.dumps([
            'and',
            ['in', 'certname',
             ['extract', 'certname',
              ['select_fact_contents',
               ['and',
                ['=', 'path', ['foo']],
                ['=', 'value', 'bar']]]]],
            ['or',
             ['=', 'name', 'foo']]]))

        self.assertEquals(node_facts, {
            'alpha': {'foo': 'bar'},
        })

    def test_query_facts_with_query_and_facts_list_regex(self):
        mock_pdb = mock.NonCallableMock()
        mock_pdb.facts = mock.Mock(return_value=[
            _FakeNode('alpha', 'foo', 'bar'),
        ])

        node_facts = self._query_facts(mock_pdb, 'foo=bar', ['/foo/'])

        mock_pdb.facts.assert_called_once_with(query=json.dumps([
            'and',
            ['in', 'certname',
             ['extract', 'certname',
              ['select_fact_contents',
               ['and',
                ['=', 'path', ['foo']],
                ['=', 'value', 'bar']]]]],
            ['or',
             ['~', 'name', 'foo']]]))

        self.assertEquals(node_facts, {
            'alpha': {'foo': 'bar'},
        })

    def test_query_facts_with_facts_list_only(self):
        mock_pdb = mock.NonCallableMock()
        mock_pdb.facts = mock.Mock(return_value=[
            _FakeNode('alpha', 'foo', 'bar'),
        ])

        node_facts = self._query_facts(mock_pdb, '', ['foo'])

        mock_pdb.facts.assert_called_once_with(query=json.dumps([
            'or',
            ['=', 'name', 'foo']]))

        self.assertEquals(node_facts, {
            'alpha': {'foo': 'bar'},
        })

    def test_query_facts_without_query_or_facts(self):
        node_facts = self._query_facts(None, '')
        self.assertTrue(node_facts is None)

    def test_query_facts_in_raw_mode(self):
        mock_pdb = mock.NonCallableMock()
        mock_pdb.facts = mock.Mock(return_value=[
            _FakeNode('alpha', 'foo', 'bar'),
        ])

        node_facts = self._query_facts(mock_pdb, 'foo=bar', raw=True)

        self.assertEquals(node_facts, mock_pdb.facts.return_value)


class TestFrontendQueryFactContents(unittest.TestCase):
    """
    Test cases targetting :func:`pypuppetdbquery.query_fact_contents`.
    """

    def _query_fact_contents(self, pdb, s, facts=None, raw=False):
        return query_fact_contents(
            pdb, s, facts, raw,
            lex_options={
                'debug': False,
                'optimize': False,
            },
            yacc_options={
                'debug': False,
                'optimize': False,
                'write_tables': False,
            })

    def test_with_query_and_facts_list(self):
        mock_pdb = mock.NonCallableMock()
        mock_pdb.fact_contents = mock.Mock(return_value=[
            {
                'value': 14,
                'certname': 'alpha',
                'environment': 'production',
                'path': ['system_uptime', 'days'],
                'name': 'system_uptime',
            },
        ])

        out = self._query_fact_contents(
            mock_pdb, 'foo=bar', ['system_uptime.days'])

        mock_pdb.fact_contents.assert_called_once_with(query=json.dumps([
            'and',
            ['in', 'certname',
             ['extract', 'certname',
              ['select_fact_contents',
               ['and',
                ['=', 'path', ['foo']],
                ['=', 'value', 'bar']]]]],
            ['or',
             ['=', 'path',
              ['system_uptime', 'days']]]]))

        self.assertEquals(out, {
            'alpha': {'system_uptime.days': 14},
        })

    def test_without_query(self):
        mock_pdb = mock.NonCallableMock()
        mock_pdb.fact_contents = mock.Mock(return_value=[
            {
                'value': 14,
                'certname': 'alpha',
                'environment': 'production',
                'path': ['system_uptime', 'days'],
                'name': 'system_uptime',
            },
        ])

        out = self._query_fact_contents(mock_pdb, '', ['system_uptime.days'])

        mock_pdb.fact_contents.assert_called_once_with(query=json.dumps([
            'or',
            ['=', 'path',
             ['system_uptime', 'days']]]))

        self.assertEquals(out, {
            'alpha': {'system_uptime.days': 14},
        })

    def test_without_either(self):
        out = self._query_fact_contents(None, '')
        self.assertTrue(out is None)

    def test_raw_output(self):
        mock_pdb = mock.NonCallableMock()
        mock_pdb.fact_contents = mock.Mock(return_value=[
            {
                'value': 14,
                'certname': 'alpha',
                'environment': 'production',
                'path': ['system_uptime', 'days'],
                'name': 'system_uptime',
            },
        ])

        out = self._query_fact_contents(
            mock_pdb, 'foo=bar', ['system_uptime.days'], True)

        mock_pdb.fact_contents.assert_called_once_with(query=json.dumps([
            'and',
            ['in', 'certname',
             ['extract', 'certname',
              ['select_fact_contents',
               ['and',
                ['=', 'path', ['foo']],
                ['=', 'value', 'bar']]]]],
            ['or',
             ['=', 'path',
              ['system_uptime', 'days']]]]))

        self.assertEquals(out, mock_pdb.fact_contents.return_value)
