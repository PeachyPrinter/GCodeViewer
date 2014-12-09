import unittest
import sys
import os
from mock import patch, Mock

sys.path.insert(0,os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0,os.path.join(os.path.dirname(__file__), '..', '..','src'))

from api.viewer import Viewer

@patch('api.viewer.AsynchronousGcodeReader')
class ViewerTest(unittest.TestCase):
    def test_load_gcode_should_read_gcode(self,mock_AsynchronousGcodeReader):
        viewer = Viewer()
        test_file = 'test_file.gcode'
        mock_asynchronous_gcode_reader = mock_AsynchronousGcodeReader.return_value
        
        viewer.load_gcode(test_file)

        self.assertEquals(test_file, mock_AsynchronousGcodeReader.call_args_list[0][0][0])
        mock_asynchronous_gcode_reader.start.assert_called_with()


if __name__ == '__main__':
    unittest.main()
