Examples
========

Basic query for nodes using :mod:`pypuppetdb`::

   import pypuppetdb
   import pypuppetdbquery

   pdb = pypuppetdb.connect()

   pdb_ast = pypuppetdbquery.parse(
       '(processorcount=4 or processorcount=8) and kernel=Linux')

   for node in pdb.nodes(query=pdb_ast):
       print(node)
