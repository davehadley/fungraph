.. _examples:

Examples
========

A single function
-----------------
Construct functions with the :py:func:`fungraph.fun`. Evaluate them with :py:meth:`fungraph.functionnode.FunctionNode.compute`.

.. literalinclude:: examples/simple_add.py

Both positional and keyword arguments may be provided.

.. literalinclude:: examples/simple_kwargs.py

Nested functions
----------------
Functions can be nested.

.. literalinclude:: examples/simple_nested.py

Getting intermediate values
---------------------------
Intermediate values are stored in the graph and may be retrieved and inspected.

.. literalinclude:: examples/simple_get.py

Recompute with modifications
----------------------------
The graph is mutable. It's nodes may be modified and the results re-computed.

.. literalinclude:: examples/simple_set.py

The graph may be cloned before modification to prevent changing the original.

.. literalinclude:: examples/simple_clone.py

Scanning an input parameter
---------------------------
You may be interested in how a function return value changes
as you change the input parameters.
This can be done with the :py:meth:`fungraph.FunctionNode.scan` method.

.. literalinclude:: examples/simple_scan.py

Dask inputs
-----------
Dask delayed objects are valid inputs to :py:func:`fungraph.fun` :py:func:`fungraph.named`.

.. literalinclude:: examples/simple_dask.py


:py:class:`dask.Delayed` objects are used internally by :py:mod:`fungraph`. Thus you may use use dask features to scale computation (eg across a HPC cluster).

.. literalinclude:: examples/dask_parallel.py