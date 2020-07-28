import unittest

from dask.base import unpack_collections, collections_to_dsk

import fungraph
from fungraph.internal.cachecallback import dsktohash


def _add_xy(x, y):
    return x + y

def _get_dsk(node):
    d = node.todelayed()
    collections, repack = unpack_collections(d, traverse=False)
    return collections_to_dsk(collections, True)

def _simplenode():
    return fungraph.fun(_add_xy,
                        x=fungraph.fun(lambda: 2),
                        y=fungraph.fun(lambda: 3),
                        )

class TestDskToHash(unittest.TestCase):

    def test_stable_repeated_iterations(self):
        def tryhash():
            return dsktohash(_get_dsk(_simplenode()))
        first = tryhash()
        for _ in range(100):
            second = tryhash()
            self.assertEqual(set(first.values()), set(second.values()))


