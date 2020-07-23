import glob
import os
import subprocess
import unittest

class TestExamples(unittest.TestCase):

    def iterexamples(self):
        dirname = os.path.dirname(os.path.abspath(__file__))
        for f in glob.glob(os.sep.join((dirname, "*.py"))):
            if __file__ not in f:
                yield f

    def test_examples_run(self):
        for fname in self.iterexamples():
            subprocess.check_call(["python3", fname])
