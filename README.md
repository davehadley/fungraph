# fungraph
 
[![Travis (.org) branch](https://img.shields.io/travis/davehadley/fungraph)](https://travis-ci.org/davehadley/fungraph)
[![Documentation Status](https://readthedocs.org/projects/fungraph/badge/?version=latest)](https://fungraph.readthedocs.io/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/fungraph)](https://pypi.org/project/fungraph/)
[![License: MIT](https://img.shields.io/pypi/l/fungraph)](https://github.com/davehadley/fungraph/blob/master/LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/davehadley/fungraph/dev)](https://github.com/davehadley/fungraph)

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

## Developer Instructions

After clone, run the shell script `post-clone.sh` which installs required pre-commit hooks.