import unittest
from argparse import ArgumentParser
from subprocess import check_output
from typing import NamedTuple, Any

from dask.base import unpack_collections, collections_to_dsk

import fungraph
from fungraph.internal.dsktohash import dsktohash


def _add_xy(x, y):
    return x + y


def _get_dsk(node):
    d = node.todelayed()
    collections, repack = unpack_collections(d, traverse=False)
    return collections_to_dsk(collections, True)


def _getsimplenode():
    return fungraph.fun(_add_xy,
                        x=fungraph.fun(lambda: 2),
                        y=fungraph.fun(lambda: 3),
                        )


def _getcollectionnode():
    return fungraph.fun(lambda x, y: (x, y),
                        [0, 1],
                        {"a": 1, "b": 2},
                        )


class TestNamedTuple1(NamedTuple):
    a: int


def _getsimplenamedtuplenode():
    return fungraph.fun(lambda x, y: (x.a, y.a),
                        TestNamedTuple1(1),
                        TestNamedTuple1(2),
                        )


class TestNamedTuple2(NamedTuple):
    a: int
    b: dict
    c: list
    d: Any


def _getnamedtuplenode():
    return fungraph.fun(lambda x, y: (x.a, y.b),
                        TestNamedTuple2(1, {"a": 2, "b": 3}, [5, 6], "somestring"),
                        TestNamedTuple2(2, {"a": [7, 8], "b": "B"}, [5, 6], "someotherstring"),
                        )


class TestNamedTuple3(NamedTuple):
    a: list
    b: dict


class CompositeNamedTuple3(NamedTuple):
    l: TestNamedTuple3
    r: TestNamedTuple3


def _getcompositenamedtuplenode():
    return fungraph.fun(lambda x: x,
                        CompositeNamedTuple3(TestNamedTuple3([1, 2, 3], {"a": 1, "b": 2}),
                                             TestNamedTuple3([4, 5, 6], {"c": 4, "d": 5}), ),
                        )


class A:
    def __init__(self, a):
        self.a = a


def _getuserdefinedclassnode():
    return fungraph.fun(lambda x, y: x.a + y.a,
                        A(1),
                        A(2),
                        )


def _getnode(type: int):
    return {0: _getsimplenode(),
            1: _getcollectionnode(),
            2: _getsimplenamedtuplenode(),
            3: _getnamedtuplenode(),
            4: _getcompositenamedtuplenode(),
            5: _getuserdefinedclassnode(),
            }[type]


def _typerange():
    return range(6)


def _simplehash(type: int):
    return dsktohash(_get_dsk(_getnode(type)))


class TestDskToHash(unittest.TestCase):

    def test_stable_repeated_iterations(self):
        for type in _typerange():
            with self.subTest(type=type):
                def tryhash(type=type):
                    return dsktohash(_get_dsk(_getnode(type=type)))

                first = tryhash(type)
                for _ in range(10):
                    second = tryhash(type)
                    self.assertEqual(set(first.values()), set(second.values()))

    def test_stable_repeated_iterations_multiprocess(self):
        for type in _typerange():
            with self.subTest(type=type):
                tothers = [eval(check_output(["python", "test_dsktohash.py", str(type)]).splitlines()[-1]) for _ in
                           range(3)]
                for t2 in tothers:
                    self.assertEqual(set(t2.values()), set(_simplehash(type).values()))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("type", type=int, default=0)
    args = parser.parse_args()
    print(dsktohash(_get_dsk(_getnode(args.type))))
