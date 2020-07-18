import operator
import unittest

import fungraph


def _add_xy(x, y):
    return x + y


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

    def test_set_by_name(self):
        node = fungraph.named("add", operator.add,
                              fungraph.named("a", lambda: 1),
                              fungraph.named("b", lambda: 2),
                              )
        aprime = fungraph.named("aprime", lambda: 3)
        node["a"] = aprime
        self.assertEqual(node.compute(), 5)
        with self.assertRaises(KeyError):
            node["a"]
        return

    def test_retrieve_by_wrong_name_raises_keyerror(self):
        node = fungraph.named("add", operator.add,
                              fungraph.named("a", lambda: 1),
                              fungraph.named("b", lambda: 2),
                              )
        with self.assertRaises(KeyError):
            node["c"]
        return

    def test_set_by_wrong_name_raises_keyerror(self):
        node = fungraph.named("add", operator.add,
                              fungraph.named("a", lambda: 1),
                              fungraph.named("b", lambda: 2),
                              )
        with self.assertRaises(KeyError):
            node["c"] = fungraph.named("c", lambda: 3)
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

    def test_get_nameclash_with_named(self):
        node = fungraph.fun(operator.add,
                            fungraph.named("x", lambda: 1),
                            fungraph.named("x", lambda: 2),
                            )
        x = node["x"]
        # return first found result
        self.assertEqual(node.compute(), 3)
        self.assertEqual(x.compute(), 1)
        self.assertEqual(x.name, "x")
        return

    def test_set_nameclash_with_named(self):
        node = fungraph.fun(operator.add,
                            fungraph.named("x", lambda: 1),
                            fungraph.named("x", lambda: 2),
                            )
        node["x"] = fungraph.named("x", lambda: 3)
        # set first found result
        self.assertEqual(node.compute(), 5)
        return

    def test_get_nameclash_with_kwargument(self):
        node = fungraph.fun(_add_xy,
                            x=fungraph.named("y", lambda: 1),
                            y=fungraph.named("x", lambda: 2),
                            )
        x = node["x"]
        # prefer arguments over named
        self.assertEqual(node.compute(), 3)
        self.assertEqual(x.compute(), 1)
        self.assertEqual(x.name, "y")
        return

    def test_set_nameclash_with_kwargument(self):
        node = fungraph.fun(_add_xy,
                            x=fungraph.named("y", lambda: 1),
                            y=fungraph.named("x", lambda: 2),
                            )
        node["x"] = fungraph.named("z", lambda: 3)
        # prefer arguments over named
        self.assertEqual(node.compute(), 5)
        return

    def test_get_nameclash_with_kwargument_explicit(self):
        node = fungraph.fun(_add_xy,
                            x=fungraph.named("y", lambda: 1),
                            y=fungraph.named("x", lambda: 2),
                            )
        x = node[fungraph.Name("x")]
        y = node[fungraph.KeywordArgument("x")]
        self.assertEqual(x.compute(), 2)
        self.assertEqual(x.name, "x")
        self.assertEqual(y.compute(), 1)
        self.assertEqual(y.name, "y")
        return

    def test_set_nameclash_with_kwargument_explicit(self):
        node = fungraph.fun(_add_xy,
                            x=fungraph.named("y", lambda: 1),
                            y=fungraph.named("x", lambda: 2),
                            )
        node[fungraph.Name("x")] = fungraph.named("z", lambda: 3)
        node[fungraph.KeywordArgument("x")] = fungraph.named("w", lambda: 4)
        self.assertEqual(node["x"].compute(), 4)
        self.assertEqual(node["x"].name, "w")
        self.assertEqual(node["y"].compute(), 3)
        self.assertEqual(node["y"].name, "z")
        return

    def test_retrieve_by_path(self):
        node = fungraph.named("add", operator.add,
                              fungraph.named("mul1", operator.mul, fungraph.named("one", lambda: 1),
                                             fungraph.named("two", lambda: 2)),
                              fungraph.named("mul2", operator.mul, fungraph.named("three", lambda: 3),
                                             fungraph.named("four", lambda: 4)),
                              )
        one = node["mul1/one"]
        two = node["mul1/two"]
        three = node["mul2/three"]
        four = node["mul2/four"]
        self.assertEqual(one.compute(), 1)
        self.assertEqual(two.compute(), 2)
        self.assertEqual(three.compute(), 3)
        self.assertEqual(four.compute(), 4)
        return

    def test_set_by_path(self):
        node = fungraph.named("add", operator.add,
                              fungraph.named("mul1", operator.mul, fungraph.named("one", lambda: 1),
                                             fungraph.named("two", lambda: 2)),
                              fungraph.named("mul2", operator.mul, fungraph.named("three", lambda: 3),
                                             fungraph.named("four", lambda: 4)),
                              )
        node["mul1/one"] = fungraph.named("five", lambda: 5)
        node["mul1/two"] = fungraph.named("size", lambda: 6)
        node["mul2/three"] = fungraph.named("seven", lambda: 7)
        node["mul2/four"] = fungraph.named("eight", lambda: 8)
        self.assertEqual(node.compute(), 5 * 6 + 7 * 8)
        return

    def test_get_all(self):
        node = fungraph.named("add", operator.add,
                              fungraph.named("p1", operator.mul,
                                             fungraph.named("a", lambda: 1),
                                             fungraph.named("b", lambda: 2),
                                             ),
                              fungraph.named("p2", operator.mul,
                                             fungraph.named("a", lambda: 3),
                                             fungraph.named("b", lambda: 4),
                                             )
                              )
        bs = node.getall("b")
        self.assertEqual([b.compute() for b in bs], [2, 4])
