import operator
import unittest

import fungraph


class TestNamedFunctionNode(unittest.TestCase):
    def test_constructor(self):
        return fungraph.named("name", lambda: None)

    def test_simple_named_graph(self):
        node = fungraph.named("add", operator.add, 1, 2)
        self.assertEqual(node.compute(), 3)
        self.assertEqual(node.name, "add")
        return

    def test_retrieve_by_name(self):
        node = fungraph.named("add", operator.add,
                              fungraph.named("a", lambda: 1),
                              fungraph.named("b", lambda: 2),
                              )
        a = node["a"]
        b = node["b"]
        self.assertEqual(a.compute(), 1)
        self.assertEqual(b.compute(), 2)
        self.assertEqual(a.name, "a")
        self.assertEqual(b.name, "b")
        return

    def test_retrieve_by_wrong_name_raises_keyerror(self):
        node = fungraph.named("add", operator.add,
                              fungraph.named("a", lambda: 1),
                              fungraph.named("b", lambda: 2),
                              )
        with self.assertRaises(KeyError):
            node["c"]
        return

    def test_mixed_named_unnamed_graph(self):
        node = fungraph.fun(operator.add,
                              fungraph.fun(lambda: 1),
                              fungraph.named("b", lambda: 2),
                              )
        b = node["b"]
        self.assertEqual(node.compute(), 3)
        self.assertEqual(b.compute(), 2)
        self.assertEqual(b.name, "b")
        return
