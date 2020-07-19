.. _examples:

Examples
========

A single function
-----------------
Construct functions with the :py:function:`fungraph.fun`. Evaluate them with :py:method:`fungraph.FunctionNode.compute`.
.. literalinclude:: examples/simple_add.py

Both positional and keyword arguments may be provided
.. literalinclude:: examples/simple_kwargs.py

Nested functions
----------------
Functions can be nested.
.. literalinclude:: examples/simple_nested.py

Getting Intermediate Values
---------------------------
Intermediate values are stored in the graph and get be retrieved.
.. literalinclude:: examples/simple_get.py

Recompute with Modifications
----------------------------
The graph is mutable. It's nodes may be modified and the results re-computed.
.. literalinclude:: examples/simple_set.py

The graph may be cloned before modification to prevent changing the original.
.. literalinclude:: examples/simple_clone.py

Scanning an Input Parameter
---------------------------
You may be interested in how a function return value changes
as you change the input parameters.
This can be done with the :py:method:`fungraph.FunctionNode.scan` method.
..literalinclude:: examples/simple_scan.py

Dask Inputs
-----------
Dask delayed objected are valid inputs to :py:function:`fungraph.fun` :py:function:`fungraph.named`.
..literalinclude:: examples/simple_dask.py
:py:mod:fungraph uses `dask.delayed` internally. Thus you may use use dask features to scale computation (eg across a HPC cluster).
..literalinclude:: examples/dask_parallel.py