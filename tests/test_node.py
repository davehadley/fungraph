import operator
import tempfile
import timeit
import unittest
from time import sleep
from typing import Any, Callable

import graci


def _slow_identity(x: Any, waitseconds: float = 1) -> Any:
    sleep(waitseconds)
    return x


def _timeonce(f: Callable[[], Any]) -> float:
    return timeit.timeit(f, number=1)


def _add_xy(x: int, y: int):
    return x + y


class TestNode(unittest.TestCase):

    def test_constructor(self):
        f = graci.node(lambda: None)
        self.assertIsNone(f.compute())

    def test_integer_arguments(self):
        result = graci.node(operator.add, 2, 3).compute()
        self.assertEqual(result, 5)

    def test_node_arguments(self):
        result = graci.node(operator.add,
                            graci.node(lambda: 2),
                            graci.node(lambda: 3),
                            ).compute()
        self.assertEqual(result, 5)

    def test_integer_keywordarguments(self):
        result = graci.node(_add_xy, x=2, y=3).compute()
        self.assertEqual(result, 5)

    def test_node_keywordarguments(self):
        result = graci.node(_add_xy,
                            x=graci.node(lambda: 2),
                            y=graci.node(lambda: 3),
                            ).compute()
        self.assertEqual(result, 5)

    def test_integer_mixedarguments(self):
        result = graci.node(_add_xy, 2, y=3).compute()
        self.assertEqual(result, 5)

    def test_node_mixedarguments(self):
        result = graci.node(_add_xy,
                            graci.node(lambda: 2),
                            y=graci.node(lambda: 3),
                            ).compute()
        self.assertEqual(result, 5)

    def test_cache(self):
        cachedir = tempfile.mkdtemp()
        node = graci.node(_slow_identity, 5, waitseconds=1)
        f = lambda: node.compute(cachedir=cachedir)
        t1 = _timeonce(f)
        t2 = _timeonce(f)
        self.assertGreater(t1, 0.5)
        self.assertLess(t2, 0.5)

    def test_modify_arguments(self):
        node = graci.node(operator.add, 2, 3)
        result1 = node.compute()
        node[1] = 4
        result2 = node.compute()
        self.assertEqual(result1, 5)
        self.assertEqual(result2, 6)

    def test_modify_keywordarguments(self):
        node = graci.node(_add_xy, x=2, y=3)
        result1 = node.compute()
        node["y"] = 4
        result2 = node.compute()
        self.assertEqual(result1, 5)
        self.assertEqual(result2, 6)
