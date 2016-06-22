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

from distutils.util import convert_path
from setuptools import setup, find_packages

# Read the version number from version.py.
main_ns = {}
ver_path = convert_path('pypuppetdbquery/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setup(
    name='pypuppetdbquery',
    version=main_ns['__version__'],
    description='A port of @dalen\'s PuppetDB Query language to Python',
    author='Chris Boot',
    author_email='bootc@bootc.net',
    license='GPL-3+',
    url='https://github.com/bootc/pypuppetdbquery/',
    packages=find_packages(),
    install_requires=[
        'ply',
        'python-dateutil',
    ],
)
