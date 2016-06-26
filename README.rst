pypuppetdbquery
===============

.. image:: https://travis-ci.org/bootc/pypuppetdbquery.svg?branch=master
    :target: https://travis-ci.org/bootc/pypuppetdbquery
    :alt: Build Statue
.. image:: https://codecov.io/gh/bootc/pypuppetdbquery/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/bootc/pypuppetdbquery
    :alt: Code Coverage
.. image:: https://readthedocs.org/projects/pypuppetdbquery/badge/?version=latest
    :target: http://pypuppetdbquery.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

A port of `Erik Dalén <https://github.com/dalen>`__'s PuppetDB Query language
to Python. This module is designed to be paired with
`pypuppetdb <https://github.com/voxpupuli/pypuppetdb>`__ but does not depend on
it directly.

This module is a Python implementation of the query language also implemented
in `puppet-puppetdbquery <https://github.com/dalen/puppet-puppetdbquery>`__ (in
Ruby) and `node-puppetdbquery
<https://github.com/dalen/node-puppetdbquery>`__ (in JavaScript/NodeJS).

Please see the `pypuppetdbquery documentation
<http://pypuppetdbquery.readthedocs.io/en/latest/>`__ courtesy of `Read the
Docs <https://readthedocs.org/>`__ and `Sphinx
<http://www.sphinx-doc.org/en/stable/>`__.

Installation
------------

You can install this package from source or from PyPi.

.. code-block:: bash

    $ pip install pypuppetdbquery

.. code-block:: bash

    $ git clone https://github.com/bootc/pypuppetdbquery
    $ python setup.py install

If you wish to hack on it clone the repository but after that run:

.. code-block:: bash

    $ pip install -r requirements.txt
    $ pip install -r requirements-dev.txt

This will install all the runtime requirements of pypuppetdbquery and
the dependencies for the test suite and generation of documentation.

Usage Example
-------------

.. code:: python

    import pypuppetdb
    import pypuppetdbquery

    pdb = pypuppetdb.connect()

    pdb_ast = pypuppetdbquery.parse(
        '(processorcount=4 or processorcount=8) and kernel=Linux')

    for node in pdb.nodes(query=pdb_ast):
        print(node)

For further examples, see the `Examples section
<http://pypuppetdbquery.readthedocs.io/en/latest/examples.html>`__ of the
`pypuppetdbquery documentation
<http://pypuppetdbquery.readthedocs.io/en/latest/>`__.

License
-------

This project is licensed under the Apache License Version 2.0.

Copyright © 2016 `Chris Boot <http://github.com/bootc>`__.
