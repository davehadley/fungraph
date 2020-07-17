# funstash

Lazily evaluated mutable graph of functions with automatically cached intermediate values. 

Features include:
* Compose a Directed Acyclic Graph (DAG) of lazily evaluated functions.
* Intermediate values are automatically cached.
* Results and arguments of all nodes in the graph are retrievable from the root node. 
* The graph is mutable allowing easy re-computation of the graph with modified function arguments.

Dependencies:
* [dask](https://dask.org/ "Dask") provides delayed functions. As all functions are dask.delayed, you can use dask features to scale computation (eg across a HPC cluster).
* [graphchain](https://pypi.org/project/graphchain/ "GraphChain") is used to provide automatic caching to disk.