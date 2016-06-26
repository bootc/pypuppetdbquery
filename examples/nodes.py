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
Query for nodes using :mod:`pypuppetdb`.
"""

import pypuppetdb
import pypuppetdbquery

pdb = pypuppetdb.connect()

pdb_ast = pypuppetdbquery.parse(
    '(processorcount=4 or processorcount=8) and kernel=Linux')

for node in pdb.nodes(query=pdb_ast):
    print(node)
