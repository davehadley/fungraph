import operator
import random
import time
import unittest
from tempfile import TemporaryDirectory

import dask.distributed
from dask import delayed

import fungraph
from tests.utils import timeonce


class TestDask(unittest.TestCase):

    def test_delayed_function(self):
        node = fungraph.fun(delayed(operator.add), 2, 3)
        self.assertEqual(node.cachedcompute(), 5)

    def test_delayed_arguments(self):
        node = fungraph.fun(operator.add, delayed(2), 3)
        self.assertEqual(node.cachedcompute(), 5)

    def test_delayed_function_and_arguments(self):
        node = fungraph.fun(delayed(operator.add), delayed(2), 3)
        self.assertEqual(node.cachedcompute(), 5)

    def test_nested_delayed_function_and_arguments(self):
        node = fungraph.fun(delayed(operator.add),
                            delayed(operator.mul)(1, 2),
                            fungraph.fun(operator.mul, 3, delayed(4))
                            )
        self.assertEqual(node.cachedcompute(), 14)

    def test_paralell(self):
        cluster = dask.distributed.LocalCluster(n_workers=8,
                                                processes=True,
                                                threads_per_worker=1,
                                                memory_limit="auto")
        with dask.distributed.Client(address=cluster):
            def slowfunc(loc):
                time.sleep(1)
                return random.gauss(loc, 1.0)

            N = 8
            args = [fungraph.fun(slowfunc, random.uniform(0.0, 1.0)) for _ in range(N)]
            jobs = fungraph.fun(lambda *args: sum(args), *args)
            t1 = timeonce(lambda: slowfunc(1.0))
            tn = timeonce(jobs.cachedcompute)
            self.assertLess(tn, (t1 * N) / 2.0)

    def test_paralell_uses_cache(self):
        cluster = dask.distributed.LocalCluster(n_workers=8,
                                                processes=True,
                                                threads_per_worker=1,
                                                memory_limit="auto")
        with dask.distributed.Client(address=cluster):
            def slowfunc(loc):
                time.sleep(1)
                return random.gauss(loc, 1.0)

            N = 8
            args = [fungraph.fun(slowfunc, random.uniform(0.0, 1.0)) for _ in range(N)]
            jobs = fungraph.fun(lambda *args: sum(args), *args)
            with TemporaryDirectory() as d:
                with fungraph.cachecontext(d):
                    t1 = timeonce(jobs.cachedcompute)
                    t2 = timeonce(jobs.cachedcompute)
            self.assertGreater(t1, 1.0)
            self.assertLess(t2, 0.5)

    def test_repr(self):
        node = fungraph.fun(delayed(operator.add), 2, 3)
        str(node)
        return
