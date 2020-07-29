# fungraph

Lazily evaluated mutable graph of functions with automatically cached intermediate values. 

Features include:
* Compose a Directed Acyclic Graph (DAG) of lazily evaluated functions.
* Intermediate values are automatically cached.
* Results and arguments of all nodes in the graph are retrievable from the root node. 
* The graph is mutable allowing easy re-computation of the graph with modified function arguments.
* [dask](https://dask.org/ "Dask") provides delayed functions. As all functions are dask.delayed, you can use dask features to scale computation (eg across a HPC cluster).

See the documentation at <https://fungraph.readthedocs.io>.

## Installation

The package is distributed via PyPi at <https://pypi.org/project/fungraph/>.
Install from the command line with:

```bash
pip install fungraph
```