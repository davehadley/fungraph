Introduction
============

:py:mod:`fungraph` provides an API to build a graph of lazily evaluated functions. Features include:
* Compose a Directed Acyclic Graph (DAG) of lazily evaluated functions.
* Intermediate values are automatically cached for fast iteration during exploration of data
   and analysis development.
* Results and arguments of all nodes in the graph are retrievable from the root node.
* The graph is cloneable and mutable allowing easy re-computation of the graph with modified function arguments.

Quick start
===========

For more see the examples in See :ref:`examples`.
