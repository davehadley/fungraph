import os
import tempfile
import time
import unittest
from multiprocessing import Pool
from subprocess import check_output

import fungraph
from tests.utils import timeonce


def _slow_add(x, y, waitseconds=1):
    time.sleep(waitseconds)
    return x + y


def _timenodeonce(node, cachedir):
    return timeonce(lambda: node.cachedcompute(cache=cachedir))


def _test_add():
    cachedir = os.sep.join((tempfile.gettempdir(), "fungraphtestmultiprocessfixeddir"))
    t = _timenodeonce(fungraph.fun(_slow_add,
                              x=fungraph.fun(lambda: 2),
                              y=fungraph.fun(lambda: 3),
                              ), cachedir=cachedir)
    print(t)
    return t


class TestFunctionNode(unittest.TestCase):

    def test_cache_multiprocessing(self):
        with tempfile.TemporaryDirectory() as cachedir:
            node = fungraph.fun(_slow_add, x=2, y=3, waitseconds=1)
            t1 = _timenodeonce(node, cachedir)
            with Pool() as p:
                tothers = p.starmap(_timenodeonce, [(node.clone(), cachedir) for _ in range(10)])
            self.assertGreater(t1, 0.5)
            for t2 in tothers:
                self.assertLess(t2, 0.5)

    def test_cache_shell(self):
        t1 = _test_add()
        tothers = [float(check_output(["python", "test_multiprocess.py"]).splitlines()[-1]) for _ in range(10)]
        for t2 in tothers:
            self.assertLess(t2, 0.5)


if __name__ == '__main__':
    _test_add()
