.. _examples:

Examples
========

A single function
-----------------
Construct functions with the :py:func:`fungraph.fun`. Evaluate them by calling the :py:class:`fungraph.functionnode.FunctionNode` object returned by :py:func:`fungraph.fun`.

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

Automatic Caching
-----------------

:py:mod:`fungraph` results and intermediate values are automatically cached.
The results are cached to disk by default, with a similar method to `graphchain <https://pypi.org/project/graphchain/>`_.
If the default caching method is not suitable for your use case (or you simply don't want to cache the results)
you may evaluate the results with :py:meth:`fungraph.functionnode.FunctionNode.compute`.

.. literalinclude:: examples/custom_caching.py

Named functions
---------------

With complex function graphs, it may be helpful to name the functions.

.. literalinclude:: examples/simple_named.py