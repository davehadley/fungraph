import operator
import time
import unittest

import dask.distributed
from dask import delayed
import numpy as np

import fungraph
from tests.utils import timeonce


class TestDask(unittest.TestCase):

    def test_delayed_function(self):
        node = fungraph.fun(delayed(operator.add), 2, 3)
        self.assertEqual(node.compute(), 5)

    def test_delayed_arguments(self):
        node = fungraph.fun(operator.add, delayed(2), 3)
        self.assertEqual(node.compute(), 5)

    def test_delayed_function_and_arguments(self):
        node = fungraph.fun(delayed(operator.add), delayed(2), 3)
        self.assertEqual(node.compute(), 5)

    def test_nested_delayed_function_and_arguments(self):
        node = fungraph.fun(delayed(operator.add),
                            delayed(operator.mul)(1, 2),
                            fungraph.fun(operator.mul, 3, delayed(4))
                            )
        self.assertEqual(node.compute(), 14)

    def test_paralell(self):
        cluster = dask.distributed.LocalCluster(n_workers=8,
                               processes=True,
                               threads_per_worker=1,
                               memory_limit="auto")
        with dask.distributed.Client(address=cluster):
            def slowfunc(loc):
                time.sleep(1)
                return np.random.normal(loc)
            N = 8
            args = [fungraph.fun(slowfunc, np.random.uniform()) for _ in range(N)]
            jobs = fungraph.fun(lambda *args: np.sum(args), *args)
            t1 = timeonce(lambda : slowfunc(1.0))
            tn = timeonce(jobs.compute)
            self.assertLess(tn, (t1*N)/2.0)
