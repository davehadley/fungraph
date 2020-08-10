"""fungraph provides an API to build and explore a graph of lazily evaluated functions.

fungraph features include:

* Compose a Directed Acyclic Graph (DAG) of lazily evaluated functions.
* Intermediate values are automatically cached for fast iteration during exploration of data and analysis development.
* Results and arguments of all nodes in the graph are retrievable from the root node.
* The graph is cloneable and mutable allowing easy re-computation of the graph with modified function arguments.

"""

from fungraph import _version

__version__ = _version.__version__
__license__ = "MIT"
__author__ = "David Hadley"


url = "https://github.com/davehadley/fungraph"

from fungraph.cache import cachecontext, Cache
from fungraph import error
from fungraph.keywordargument import KeywordArgument
from fungraph.name import Name
from fungraph.nodefactory import fun, named

__all__ = ["fun", "named", "Name", "KeywordArgument", "error", "cachecontext", "Cache"]
