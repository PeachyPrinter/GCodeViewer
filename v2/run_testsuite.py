# Test Runner

import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', ))

loader = unittest.TestLoader()
test_path = os.path.join(os.path.dirname(__file__), 'test')
suite = loader.discover(test_path, pattern='*test.py')

runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

problems = len(result.errors) + len(result.failures)
print("\nProblems: %s\n" % problems)
exit(problems)
