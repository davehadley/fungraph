import unittest

import fungraph


class TestNodeFactoryJust(unittest.TestCase):
    def test_constructor(self):
        return fungraph.named("name", lambda: None)

    def test_just_unnamed(self):
        node = fungraph.just(2)
        self.assertEqual(node.compute(), 2)
        return

    def test_just_named(self):
        node = fungraph.just(2, name="testjust")
        self.assertEqual(node.compute(), 2)
        self.assertEqual(node.name, "testjust")
        return
