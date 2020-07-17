# graci

**Gr**aph of lazily evaluated functions with **A**utomatically **C**ached **I**ntermediates.

Features include:
* Compose a Directed Acyclic Graph (DAG) of lazily evaluated functions.
* Intermediate values are automatically cached.
* All the results and arguments of any node in the graph are retrievable. 
* The graph is mutable allowing easy re-running of the graph with modified function arguments.

Dependencies:
* [dask](https://dask.org/ "Dask") provides delayed functions. As all functions are dask.delayed, you can use dask features to scale computation (eg across a HPC cluster).
* [graphchain](https://pypi.org/project/graphchain/ "GraphChain") is used to provide automatic caching to disk.