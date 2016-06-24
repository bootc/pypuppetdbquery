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

from json import dumps as json_dumps
from .evaluator import Evaluator
from .parser import Parser


def parse(s, json=True, lex_options=None, yacc_options=None):
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
    :param bool json: Whether to JSON-encode the PuppetDB AST result
    :param dict lex_options: Options passed to :func:`ply.lex.lex`
    :param dict yacc_options: Options passed to :func:`ply.yacc.yacc`
    """
    parser = Parser(lex_options=lex_options, yacc_options=yacc_options)
    evaluator = Evaluator()

    ast = parser.parse(s)
    raw = evaluator.evaluate(ast)

    if json and raw is not None:
        return json_dumps(raw)
    else:
        return raw
