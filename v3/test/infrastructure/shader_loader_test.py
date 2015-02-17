import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))


class ShaderLoaderTest(unittest.TestCase):
    def test(self):
        self.assertEquals(1, 1)

if __name__ == '__main__':
    unittest.main()
