"""graci

Graph of lazily evaluated functions with Automatically Cached Intermediates.
"""

from fungraph import _version

__version__ = _version.__version__
__license__ = "MIT"
__author__ = "David Hadley"
url = "https://github.com/davehadley/fungraph"

from fungraph.factory import fun, named

__all__ = ["fun", "named"]