import operator
import unittest

from dask import delayed

import fungraph


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
