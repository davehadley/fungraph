import unittest

import fungraph
from fungraph.internal.just import just


class TestNodeFactoryJust(unittest.TestCase):
    def test_constructor(self):
        return fungraph.named("name", lambda: None)

    def test_just_unnamed(self):
        node = just(2)
        self.assertEqual(node.cachedcompute(), 2)
        return

    def test_just_named(self):
        node = just(2, name="testjust")
        self.assertEqual(node.cachedcompute(), 2)
        self.assertEqual(node.name, "testjust")
        return
