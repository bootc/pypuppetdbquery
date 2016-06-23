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


class CompatTestCase(unittest.TestCase):
    if not hasattr(unittest.TestCase, 'assertIsInstance'):
        def assertIsInstance(self, obj, cls, msg=None):
            if not isinstance(obj, cls):
                standardMsg = '%s is not an instance of %r' \
                    % (unittest.safe_repr(obj), cls)
                self.fail(self._formatMessage(msg, standardMsg))

    if not hasattr(unittest.TestCase, 'assertIsNone'):
        def assertIsNone(self, obj, msg=None):
            if obj is not None:
                standardMsg = '%s is not None' % (unittest.safe_repr(obj),)
                self.fail(self._formatMessage(msg, standardMsg))
