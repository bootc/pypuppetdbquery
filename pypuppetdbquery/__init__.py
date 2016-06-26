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
This Python package contains a port of `Erik Dalén
<https://github.com/dalen>`__'s PuppetDB Query language to Python.

All the user-facing components of this package are intended to be found in this
module itself rather than any of the sub-modules.
"""

from collections import defaultdict
from json import dumps as json_dumps
from .evaluator import Evaluator
from .parser import Parser


def parse(s, json=True, mode='nodes', lex_options=None, yacc_options=None):
    """
    Parse a PuppetDBQuery-style query and transform it into a PuppetDB "AST"
    query.

    This function is intented to be the primary entry point for this package.
    It wraps up all the various components of this package into an easy to
    consume format. The output of this function is designed to be passed
    directly into :mod:`pypuppetdb`.

    For examples of the query syntax see `puppet-puppetdbquery
    <https://github.com/dalen/puppet-puppetdbquery>`_ and `node-puppetdbquery
    <https://github.com/dalen/node-puppetdbquery>`_ by `Erik Dalén
    <https://github.com/dalen>`_.

    :param str s: The query to parse and transform
    :param str mode: The PuppetDB endpoint being queried
    :param bool json: Whether to JSON-encode the PuppetDB AST result
    :param dict lex_options: Options passed to :func:`ply.lex.lex`
    :param dict yacc_options: Options passed to :func:`ply.yacc.yacc`
    """
    parser = Parser(lex_options=lex_options, yacc_options=yacc_options)
    evaluator = Evaluator()

    ast = parser.parse(s)
    raw = evaluator.evaluate(ast, mode=mode)

    if json and raw is not None:
        return json_dumps(raw)
    else:
        return raw


def query_facts(pdb, s, facts=None, raw=False, lex_options=None,
                yacc_options=None):
    """
    Helper to query PuppetDB for facts on nodes matching a query string.

    Adjusts the query to return only those facts requested in the function
    call.

    The fact names included in `facts` may be names or regular expressions. If
    the string starts and ends with ``/``, it is considered a regular
    expression (e.g. ``/^lsb/``).

    If `raw` is `False` (the default), the return value is a :class:`dict`
    with node names as keys containing a :class:`dict` of fact names to fact
    values. If `True` it returns raw :class:`pypuppetdb.types.Fact` objects as
    :meth:`pypuppetdb.api.BaseAPI.nodes` does.

    :param pypuppetdb.api.BaseAPI pdb: pypuppetdb connection to query from
    :param str s: The query string (may be empty to query all nodes)
    :param Sequence facts: List of fact names to search for
    :param bool raw: Whether to skip post-processing the facts into a dict
        structure
    :param dict lex_options: Options passed to :func:`ply.lex.lex`
    :param dict yacc_options: Options passed to :func:`ply.yacc.yacc`
    """
    query = parse(s, json=False, mode='facts', lex_options=lex_options,
                  yacc_options=yacc_options)

    if facts:
        factquery = ['or']
        for fact in facts:
            # Regular expression fact name?
            if fact[0] == fact[-1] == '/':
                factquery.append(['~', 'name', fact[1:-1]])
            else:
                factquery.append(['=', 'name', fact])

        if query:
            query = ['and', query, factquery]
        else:
            query = factquery

    if query is None:
        return None

    facts = pdb.facts(query=json_dumps(query))
    if raw:
        return facts

    ret = defaultdict(dict)
    for fact in facts:
        ret[fact.node][fact.name] = fact.value
    return ret
