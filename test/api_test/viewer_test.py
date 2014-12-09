import unittest
import sys
import os
from mock import patch, Mock

sys.path.insert(0,os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0,os.path.join(os.path.dirname(__file__), '..', '..','src'))

from api.viewer import Viewer

class ViewerTest(unittest.TestCase):
    def test_(self):
        pass

if __name__ == '__main__':
    unittest.main()
