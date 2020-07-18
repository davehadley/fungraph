"""fungraph

Lazily evaluated mutable graph of functions with automatically cached intermediate values.

"""

from fungraph import _version

__version__ = _version.__version__
__license__ = "MIT"
__author__ = "David Hadley"
url = "https://github.com/davehadley/fungraph"

from fungraph.nodefactory import fun, named, just

__all__ = ["fun", "named", "just"]