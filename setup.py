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

from distutils.util import convert_path
from setuptools import setup, find_packages

# Read the version number from version.py.
main_ns = {}
ver_path = convert_path('pypuppetdbquery/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

# Read the "long description" from README.rst
with open('README.rst') as readme_file:
    LONG_DESCRIPTION = readme_file.read()

setup(
    name='pypuppetdbquery',
    version=main_ns['__version__'],
    description='A port of Erik Dalén\'s PuppetDB Query language to Python',
    long_description=LONG_DESCRIPTION,
    author='Chris Boot',
    author_email='bootc@bootc.net',
    license='Apache-2.0',
    url='https://github.com/bootc/pypuppetdbquery/',
    packages=find_packages(),
    install_requires=[
        'ply',
        'python-dateutil',
    ],
)
