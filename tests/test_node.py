import operator
import unittest

import graci


class TestNode(unittest.TestCase):

    def test_constructor(self):
        f = graci.node(lambda: None)
        self.assertIsNone(f.compute())

    def test_integer_arguments(self):
        result = graci.node(operator.add, 2, 3).compute()
        self.assertEqual(result, 5)

    def test_node_arguments(self):
        result = graci.node(operator.add,
                            graci.node(lambda : 2),
                            graci.node(lambda: 3),
                            ).compute()
        self.assertEqual(result, 5)