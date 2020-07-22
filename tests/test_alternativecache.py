import operator
import time
import unittest

import fungraph
from tests.utils import timeonce


def _slow_func(*args, seconds=1):
    time.sleep(seconds)
    return args

class TestFunctionNodeWithAlternativeCache(unittest.TestCase):

    def test_cache_compute_dict(self):
        f = fungraph.fun(operator.add, 1, 2)
        cache = dict()
        f.compute(cache=cache)
        self.assertEqual(list(cache.values())[0], 3)

    def test_cache_compute_none(self):
        f = fungraph.fun(_slow_func, 1, 2)
        t1 = timeonce(lambda : f.compute(cache=None))
        t2 = timeonce(lambda : f.compute(cache=None))
        self.assertAlmostEqual(t1, t2, delta=0.1)