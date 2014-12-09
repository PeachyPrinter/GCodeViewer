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

    def test_load_gcode_should_call_layer_count_call_back(self,mock_AsynchronousGcodeReader):
        viewer = Viewer()
        test_file = 'test_file.gcode'
        mock_asynchronous_gcode_reader = mock_AsynchronousGcodeReader.return_value
        calls = []
        
        def test_call_back(layer_count):
            calls.append(layer_count)

        viewer.load_gcode(test_file, test_call_back)

        viewer_call_back = mock_AsynchronousGcodeReader.call_args_list[0][0][1]
        viewer_call_back(1)
        viewer_call_back(2)
        viewer_call_back(3)

        self.assertEquals(3, len(calls))
        self.assertEquals([1,2,3], calls)
        

    def test_load_gcode_should_call_complete_call_back(self,mock_AsynchronousGcodeReader):
        viewer = Viewer()
        test_file = 'test_file.gcode'
        mock_asynchronous_gcode_reader = mock_AsynchronousGcodeReader.return_value
        calls = []
        
        def complete_call_back(layer_count):
            calls.append(layer_count)

        viewer.load_gcode(test_file, complete_call_back = complete_call_back)

        viewer_call_back = mock_AsynchronousGcodeReader.call_args_list[0][0][1]
        viewer_call_back(1)
        viewer_call_back(2)
        viewer_call_back(3)

        complete_call_back = mock_AsynchronousGcodeReader.call_args_list[0][0][2]
        complete_call_back()

        self.assertEquals(1, len(calls))
        self.assertEquals([3], calls)

if __name__ == '__main__':
    unittest.main()
