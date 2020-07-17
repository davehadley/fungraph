"""graci

Graph of lazily evaluated functions with Automatically Cached Intermediates.
"""

from funstash import _version

__version__ = _version.__version__
__license__ = "MIT"
__author__ = "David Hadley"
url = "https://github.com/davehadley/funstash"

from funstash.node import node, named

__all__ = ["node", "named"]