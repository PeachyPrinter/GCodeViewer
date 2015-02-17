import unittest
import os
import sys

test_path = os.path.join(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(test_path, '..', 'src'))
sys.path.insert(0, test_path)
print("Test path: %s" % test_path)

loader = unittest.TestLoader()
suite = loader.discover(test_path, pattern='*test.py')

runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

problems = len(result.errors) + len(result.failures)
print("\nProblems: %s\n" % problems)
exit(problems)
