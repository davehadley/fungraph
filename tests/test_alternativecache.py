import operator
import unittest

import fungraph


class TestFunctionNodeWithAlternativeCache(unittest.TestCase):

    def test_cache_compute(self):
        f = fungraph.fun(operator.add, 1, 2)
        cache = dict()
        f.compute(cache=cache)
        self.assertEqual(list(cache.values())[0], 3)
