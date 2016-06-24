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
import unittest

from pypuppetdbquery import parse


class TestFrontend(unittest.TestCase):
    """
    Test cases targetting :mod:`pypuppetdbquery`, and particularly
    :func:`pypuppetdbquery.parse`.
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
