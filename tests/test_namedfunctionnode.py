import operator
import unittest

import fungraph


class TestNamedFunctionNode(unittest.TestCase):
    def test_constructor(self):
        return fungraph.named("name", lambda: None)

    def test_simple_named_graph(self):
        node = fungraph.named("add", operator.add,
                              fungraph.named("a", lambda: 1),
                              fungraph.named("a", lambda: 2),
                              )
        return
