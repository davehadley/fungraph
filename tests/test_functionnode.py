import operator
import pickle
import shelve
import tempfile
import timeit
import unittest
from time import sleep
from typing import Any, Callable

import cloudpickle

import fungraph


def _slow_identity(x: Any, waitseconds: float = 1) -> Any:
    sleep(waitseconds)
    return x


def _timeonce(f: Callable[[], Any]) -> float:
    return timeit.timeit(f, number=1)


def _add_xy(x: int, y: int):
    return x + y


def _mul_xy(x: int, y: int):
    return x * y


class TestFunctionNode(unittest.TestCase):

    def test_constructor(self):
        f = fungraph.fun(lambda: None)
        self.assertIsNone(f.compute())

    def test_integer_arguments(self):
        result = fungraph.fun(operator.add, 2, 3).compute()
        self.assertEqual(result, 5)

    def test_node_arguments(self):
        result = fungraph.fun(operator.add,
                              fungraph.fun(lambda: 2),
                              fungraph.fun(lambda: 3),
                              ).compute()
        self.assertEqual(result, 5)

    def test_integer_keywordarguments(self):
        result = fungraph.fun(_add_xy, x=2, y=3).compute()
        self.assertEqual(result, 5)

    def test_node_keywordarguments(self):
        result = fungraph.fun(_add_xy,
                              x=fungraph.fun(lambda: 2),
                              y=fungraph.fun(lambda: 3),
                              ).compute()
        self.assertEqual(result, 5)

    def test_path_arguments(self):
        node = fungraph.fun(_add_xy,
                            fungraph.fun(_mul_xy, 1, 2),
                            fungraph.fun(_mul_xy, 3, 4),
                            )
        self.assertEqual(node[0][0], 1)
        self.assertEqual(node[0][1], 2)
        self.assertEqual(node[1][0], 3)
        self.assertEqual(node[1][1], 4)
        self.assertEqual(node["0/0"], 1)
        self.assertEqual(node["0/1"], 2)
        self.assertEqual(node["1/0"], 3)
        self.assertEqual(node["1/1"], 4)

    def test_path_kwarguments(self):
        node = fungraph.fun(_add_xy,
                            x=fungraph.fun(_mul_xy, x=1, y=2),
                            y=fungraph.fun(_mul_xy, x=3, y=4),
                            )
        self.assertEqual(node["x"]["x"], 1)
        self.assertEqual(node["x"]["y"], 2)
        self.assertEqual(node["y"]["x"], 3)
        self.assertEqual(node["y"]["y"], 4)
        self.assertEqual(node["x/x"], 1)
        self.assertEqual(node["x/y"], 2)
        self.assertEqual(node["y/x"], 3)
        self.assertEqual(node["y/y"], 4)

    def test_integer_mixedarguments(self):
        result = fungraph.fun(_add_xy, 2, y=3).compute()
        self.assertEqual(result, 5)

    def test_node_mixedarguments(self):
        result = fungraph.fun(_add_xy,
                              fungraph.fun(lambda: 2),
                              y=fungraph.fun(lambda: 3),
                              ).compute()
        self.assertEqual(result, 5)

    def test_cache(self):
        cachedir = tempfile.mkdtemp()
        node = fungraph.fun(_slow_identity, 5, waitseconds=1)
        f = lambda: node.compute(cachedir=cachedir)
        t1 = _timeonce(f)
        t2 = _timeonce(f)
        self.assertGreater(t1, 0.5)
        self.assertLess(t2, 0.5)

    def test_modify_arguments(self):
        node = fungraph.fun(operator.add, 2, 3)
        result1 = node.compute()
        node[1] = 4
        result2 = node.compute()
        self.assertEqual(result1, 5)
        self.assertEqual(result2, 6)

    def test_modify_nonexistant_argument_raises_keyerror(self):
        node = fungraph.fun(operator.add, 2, 3)
        with self.assertRaises(KeyError):
            node[2] = 4

    def test_modify_nonexistant_kwargument_raises_keyerror(self):
        node = fungraph.fun(_add_xy, x=2, y=3)
        with self.assertRaises(KeyError):
            node["z"] = 4

    def test_modify_keywordarguments(self):
        node = fungraph.fun(_add_xy, x=2, y=3)
        result1 = node.compute()
        node["y"] = 4
        result2 = node.compute()
        self.assertEqual(result1, 5)
        self.assertEqual(result2, 6)

    def test_modify_nodearguments(self):
        node = fungraph.fun(operator.add,
                            fungraph.fun(lambda: 2),
                            fungraph.fun(lambda: 3)
                            )
        result1 = node.compute()
        node[1] = fungraph.fun(lambda: 4)
        result2 = node.compute()
        self.assertEqual(result1, 5)
        self.assertEqual(result2, 6)

    def test_modify_path_arguments(self):
        node = fungraph.fun(_add_xy,
                            fungraph.fun(_mul_xy, 1, y=2),
                            y=fungraph.fun(_mul_xy, 3, y=4),
                            )
        node["0/0"] = 10
        node["0/y"] = 20
        node["y/0"] = 30
        node["y/y"] = 40
        self.assertEqual(node[0][0], 10)
        self.assertEqual(node[0]["y"], 20)
        self.assertEqual(node["y"][0], 30)
        self.assertEqual(node["y"]["y"], 40)
        self.assertEqual(node["0/0"], 10)
        self.assertEqual(node["0/y"], 20)
        self.assertEqual(node["y/0"], 30)
        self.assertEqual(node["y/y"], 40)

    def test_pickleable(self):
        node1 = fungraph.fun(_add_xy, x=2, y=3)
        node2 = pickle.loads(pickle.dumps(node1))
        self.assertEqual(node1.compute(), node2.compute())

    def test_cloudpickle(self):
        node1 = fungraph.fun(_add_xy, x=fungraph.fun(lambda: 2), y=3)
        node2 = cloudpickle.loads(cloudpickle.dumps(node1))
        self.assertEqual(node1.compute(), node2.compute())

    def test_shelveable(self):
        node1 = fungraph.fun(_add_xy, x=2, y=3)
        with shelve.open("testshelf.shelf.db") as s:
            s["test_node"] = node1
        with shelve.open("testshelf.shelf.db") as s:
            node2 = s["test_node"]
        self.assertEqual(node1.compute(), node2.compute())

    def test_scan_oneargument(self):
        node = fungraph.fun(operator.mul, 2, 2)
        scan = node.scan({0: [1, 2, 3, 4]})
        self.assertEqual(node.compute(), 4)
        self.assertEqual(scan.compute(), (2, 4, 6, 8))

    def test_scan_twoarguments(self):
        node = fungraph.fun(operator.mul, 2, 2)
        scan = node.scan({0: [1, 2, 3, 4], 1: [1, 2, 3, 4]})
        self.assertEqual(node.compute(), 4)
        self.assertEqual(scan.compute(), (1, 4, 9, 16))

    def test_scan_twoarguments_mismatched_length_raises(self):
        node = fungraph.fun(operator.mul, 2, 2)
        with self.assertRaises(ValueError):
            node.scan({0: [1, 2, 3, 4], 1: [1, 2, 3, 4, 5]})

    def test_scan_onekwargument(self):
        node = fungraph.fun(_mul_xy, x=2, y=2)
        scan = node.scan({"x": [1, 2, 3, 4]})
        self.assertEqual(node.compute(), 4)
        self.assertEqual(scan.compute(), (2, 4, 6, 8))

    def test_scan_twokwargument(self):
        node = fungraph.fun(_mul_xy, x=2, y=2)
        scan = node.scan({"x": [1, 2, 3, 4], "y": [1, 2, 3, 4]})
        self.assertEqual(node.compute(), 4)
        self.assertEqual(scan.compute(), (1, 4, 9, 16))

    def test_scan_pathargument(self):
        node = fungraph.fun(_add_xy,
                            x=fungraph.fun(_mul_xy, x=1, y=2),
                            y=fungraph.fun(_mul_xy, x=3, y=4),
                            )
        scan = node.scan({"x/x": [1, 2, 3], "y/x": [1, 2, 3]})
        self.assertEqual(node.compute(), 2 + 3 * 4)
        self.assertEqual(scan.compute(), (1 * 2 + 1 * 4, 2 * 2 + 2 * 4, 3 * 2 + 3 * 4))

    def test_clone(self):
        node = fungraph.fun(operator.add,
                            fungraph.fun(lambda: 2),
                            fungraph.fun(lambda: 3),
                            )
        clone = node.clone()
        self.assertEqual(node.compute(), clone.compute())

    def test_modify_clone(self):
        node = fungraph.fun(operator.add,
                            fungraph.fun(lambda: 2),
                            fungraph.fun(lambda: 3),
                            )
        clone = node.clone()
        clone[1] = fungraph.fun(lambda: 4)
        self.assertEqual(node.compute(), 5)
        self.assertEqual(clone.compute(), 6)

    def test_clone_reuses_cache(self):
        cachedir = tempfile.mkdtemp()
        node = fungraph.fun(operator.add,
                            fungraph.fun(_slow_identity, 2, waitseconds=1),
                            fungraph.fun(_slow_identity, 3, waitseconds=1),
                            )
        clone = node.clone()
        nodefun = lambda: node.compute(cachedir=cachedir)
        clonefun = lambda: clone.compute(cachedir=cachedir)
        tn1 = _timeonce(nodefun)
        tn2 = _timeonce(nodefun)
        tc1 = _timeonce(clonefun)
        self.assertGreater(tn1, 0.5)
        self.assertLess(tn2, 0.5)
        self.assertLess(tc1, 0.5)