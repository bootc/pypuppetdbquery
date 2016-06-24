# pypuppetdbquery

[![Build Status](https://travis-ci.org/bootc/pypuppetdbquery.svg?branch=master)](https://travis-ci.org/bootc/pypuppetdbquery)
[![codecov](https://codecov.io/gh/bootc/pypuppetdbquery/branch/master/graph/badge.svg)](https://codecov.io/gh/bootc/pypuppetdbquery)
[![Documentation Status](https://readthedocs.org/projects/pypuppetdbquery/badge/?version=latest)](http://pypuppetdbquery.readthedocs.io/en/latest/?badge=latest)

A port of [Erik Dalén](https://github.com/dalen)'s PuppetDB Query language to
Python. This module is designed to be paired with
[pypuppetdb](https://github.com/voxpupuli/pypuppetdb) but does not depend on it
directly.

This module is a Python implementation of the query language also implemented
in [puppet-puppetdbquery](https://github.com/dalen/puppet-puppetdbquery) (in
Ruby) and [node-puppetdbquery](``https://github.com/dalen/node-puppetdbquery) (in
JavaScript/NodeJS).

Please see the
[pypuppetdbquery documentation](http://pypuppetdbquery.readthedocs.io/en/latest/?badge=latest)
courtesy of [Read the Docs](https://readthedocs.org/) and
[Sphinx](http://www.sphinx-doc.org/en/stable/).

## Installation

You can install this package from source or from PyPi.

```sh
$ pip install pypuppetdbquery
```

```sh
$ git clone https://github.com/bootc/pypuppetdbquery
$ python setup.py install
```

If you wish to hack on it clone the repository but after that run:

```sh
$ pip install -r requirements.txt
$ pip install -r requirements-dev.txt
```

This will install all the runtime requirements of pypuppetdbquery and the
dependencies for the test suite and generation of documentation.

## Usage Example

```python
import pypuppetdb
import pypuppetdbquery

pdb = pypuppetdb.connect()

pdb_ast = pypuppetdbquery.parse(
    '(processorcount=4 or processorcount=8) and kernel=Linux')

for node in pdb.nodes(query=pdb_ast):
    print(node)
```

## License

This project is licensed under the Apache License Version 2.0.

Copyright © 2016 [Chris Boot](http://github.com/bootc).
