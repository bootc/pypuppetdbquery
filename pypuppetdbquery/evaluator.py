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

# from . import ast


class EvaluationException(Exception):
    def __init__(self, message):
        super(EvaluationException, self).__init__(message)


class Evaluator(object):
    def __init__(self):
        pass

    def evaluate(self, ast):
        pass
