import operator
import tempfile
import unittest

import fungraph


def _add_xy(x, y):
    return x + y


class TestNamedFunctionNode(unittest.TestCase):
    def test_constructor(self):
        return fungraph.named("name", lambda: None)

    def test_simple_named_graph(self):
        node = fungraph.named("add", operator.add, 1, 2)
        self.assertEqual(node.cachedcompute(), 3)
        self.assertEqual(node.name, "add")
        return

    def test_retrieve_by_name(self):
        node = fungraph.named("add", operator.add,
                              fungraph.named("a", lambda: 1),
                              fungraph.named("b", lambda: 2),
                              )
        a = node["a"]
        b = node["b"]
        self.assertEqual(a.cachedcompute(), 1)
        self.assertEqual(b.cachedcompute(), 2)
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
        self.assertEqual(node.cachedcompute(), 5)
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
        self.assertEqual(node.cachedcompute(), 3)
        self.assertEqual(b.cachedcompute(), 2)
        self.assertEqual(b.name, "b")
        return

    def test_get_nameclash_with_named(self):
        node = fungraph.fun(operator.add,
                            fungraph.named("x", lambda: 1),
                            fungraph.named("x", lambda: 2),
                            )
        x = node["x"]
        # return first found result
        self.assertEqual(node.cachedcompute(), 3)
        self.assertEqual(x.cachedcompute(), 1)
        self.assertEqual(x.name, "x")
        return

    def test_set_nameclash_with_named(self):
        node = fungraph.fun(operator.add,
                            fungraph.named("x", lambda: 1),
                            fungraph.named("x", lambda: 2),
                            )
        node["x"] = fungraph.named("x", lambda: 3)
        # set first found result
        self.assertEqual(node.cachedcompute(), 5)
        return

    def test_get_nameclash_with_kwargument(self):
        node = fungraph.fun(_add_xy,
                            x=fungraph.named("y", lambda: 1),
                            y=fungraph.named("x", lambda: 2),
                            )
        x = node["x"]
        # prefer arguments over named
        self.assertEqual(node.cachedcompute(), 3)
        self.assertEqual(x.cachedcompute(), 1)
        self.assertEqual(x.name, "y")
        return

    def test_set_nameclash_with_kwargument(self):
        node = fungraph.fun(_add_xy,
                            x=fungraph.named("y", lambda: 1),
                            y=fungraph.named("x", lambda: 2),
                            )
        node["x"] = fungraph.named("z", lambda: 3)
        # prefer arguments over named
        self.assertEqual(node.cachedcompute(), 5)
        return

    def test_get_nameclash_with_kwargument_explicit(self):
        node = fungraph.fun(_add_xy,
                            x=fungraph.named("y", lambda: 1),
                            y=fungraph.named("x", lambda: 2),
                            )
        x = node[fungraph.Name("x")]
        y = node[fungraph.KeywordArgument("x")]
        self.assertEqual(x.cachedcompute(), 2)
        self.assertEqual(x.name, "x")
        self.assertEqual(y.cachedcompute(), 1)
        self.assertEqual(y.name, "y")
        return

    def test_set_nameclash_with_kwargument_explicit(self):
        node = fungraph.fun(_add_xy,
                            x=fungraph.named("y", lambda: 1),
                            y=fungraph.named("x", lambda: 2),
                            )
        node[fungraph.Name("x")] = fungraph.named("z", lambda: 3)
        node[fungraph.KeywordArgument("x")] = fungraph.named("w", lambda: 4)
        self.assertEqual(node["x"].cachedcompute(), 4)
        self.assertEqual(node["x"].name, "w")
        self.assertEqual(node["y"].cachedcompute(), 3)
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
        self.assertEqual(one.cachedcompute(), 1)
        self.assertEqual(two.cachedcompute(), 2)
        self.assertEqual(three.cachedcompute(), 3)
        self.assertEqual(four.cachedcompute(), 4)
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
        self.assertEqual(node.cachedcompute(), 5 * 6 + 7 * 8)
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
        self.assertEqual([b.cachedcompute() for b in bs], [2, 4])

    def test_set_all(self):
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
        node.setall("b", fungraph.named("c", lambda: 5))
        self.assertEqual(node.cachedcompute(), 1 * 5 + 3 * 5)

    def test_identical_function(self):
        cachedir = tempfile.mkdtemp()
        f = fungraph.named("add", operator.add,
                           fungraph.named("left", operator.mul, 2, 2),
                           fungraph.named("right", operator.mul, 2, 2),
                           )
        self.assertEqual(f.cachedcompute(cache=cachedir), 8)

    def test_repr(self):
        name = "name"
        node = fungraph.named(name, operator.add, 1, 2)
        self.assertTrue(name in str(node))
