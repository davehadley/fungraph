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

    def test_cache(self):
        cachedir = tempfile.mkdtemp()
        node = graci.node(_slow_identity, 5, waitseconds=1)
        f = lambda: node.compute(cachedir=cachedir)
        t1 = _timeonce(f)
        t2 = _timeonce(f)
        self.assertGreater(t1, 0.5)
        self.assertLess(t2, 0.5)
