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

    def test_get_layers_returns_all_layers(self, mock_AsynchronousGcodeReader):
        viewer = Viewer()
        test_file = 'test_file.gcode'
        mock_asynchronous_gcode_reader = mock_AsynchronousGcodeReader.return_value
        viewer.load_gcode(test_file)
        viewer_call_back = mock_AsynchronousGcodeReader.call_args_list[0][0][1]
        for i in range(0,100):
            viewer_call_back('Layer: %s' % i)
        complete_call_back = mock_AsynchronousGcodeReader.call_args_list[0][0][2]
        complete_call_back()

        layers = viewer.get_layers()

        self.assertEquals(100,len(layers))
        self.assertEquals(layers[0], 'Layer: 0')

    def test_get_layers_returns_all_layers_after_start(self, mock_AsynchronousGcodeReader):
        viewer = Viewer()
        test_file = 'test_file.gcode'
        mock_asynchronous_gcode_reader = mock_AsynchronousGcodeReader.return_value
        viewer.load_gcode(test_file)
        viewer_call_back = mock_AsynchronousGcodeReader.call_args_list[0][0][1]
        for i in range(0,100):
            viewer_call_back('Layer: %s' % i)
        complete_call_back = mock_AsynchronousGcodeReader.call_args_list[0][0][2]
        complete_call_back()

        layers = viewer.get_layers(50)

        self.assertEquals(50,len(layers))
        self.assertEquals(layers[0], 'Layer: 50')
        self.assertEquals(layers[49], 'Layer: 99')

    def test_get_layers_returns_all_layers_after_start_before_end(self, mock_AsynchronousGcodeReader):
        viewer = Viewer()
        test_file = 'test_file.gcode'
        mock_asynchronous_gcode_reader = mock_AsynchronousGcodeReader.return_value
        viewer.load_gcode(test_file)
        viewer_call_back = mock_AsynchronousGcodeReader.call_args_list[0][0][1]
        for i in range(0,100):
            viewer_call_back('Layer: %s' % i)
        complete_call_back = mock_AsynchronousGcodeReader.call_args_list[0][0][2]
        complete_call_back()

        layers = viewer.get_layers(50,60)

        self.assertEquals(10,len(layers))
        self.assertEquals(layers[0], 'Layer: 50')
        self.assertEquals(layers[9], 'Layer: 59')

    def test_get_layers_returns_all_layers_after_start_before_end_skipping(self, mock_AsynchronousGcodeReader):
        viewer = Viewer()
        test_file = 'test_file.gcode'
        mock_asynchronous_gcode_reader = mock_AsynchronousGcodeReader.return_value
        viewer.load_gcode(test_file)
        viewer_call_back = mock_AsynchronousGcodeReader.call_args_list[0][0][1]
        for i in range(0,100):
            viewer_call_back('Layer: %s' % i)
        complete_call_back = mock_AsynchronousGcodeReader.call_args_list[0][0][2]
        complete_call_back()

        layers = viewer.get_layers(50,60,5)

        self.assertEquals(2,len(layers))
        self.assertEquals(layers[0], 'Layer: 50')
        self.assertEquals(layers[1], 'Layer: 55')


    def test_get_layers_returns_all_layers_if_start_is_negitive(self, mock_AsynchronousGcodeReader):
        viewer = Viewer()
        test_file = 'test_file.gcode'
        mock_asynchronous_gcode_reader = mock_AsynchronousGcodeReader.return_value
        viewer.load_gcode(test_file)
        viewer_call_back = mock_AsynchronousGcodeReader.call_args_list[0][0][1]
        for i in range(0,100):
            viewer_call_back('Layer: %s' % i)
        complete_call_back = mock_AsynchronousGcodeReader.call_args_list[0][0][2]
        complete_call_back()

        layers = viewer.get_layers(-50)

        self.assertEquals(100,len(layers))
        self.assertEquals(layers[0], 'Layer: 0')

    def test_get_layers_returns_all_layers_if_end_larger_then_layers(self, mock_AsynchronousGcodeReader):
        viewer = Viewer()
        test_file = 'test_file.gcode'
        mock_asynchronous_gcode_reader = mock_AsynchronousGcodeReader.return_value
        viewer.load_gcode(test_file)
        viewer_call_back = mock_AsynchronousGcodeReader.call_args_list[0][0][1]
        for i in range(0,100):
            viewer_call_back('Layer: %s' % i)
        complete_call_back = mock_AsynchronousGcodeReader.call_args_list[0][0][2]
        complete_call_back()

        layers = viewer.get_layers(0,1000)

        self.assertEquals(100,len(layers))
        self.assertEquals(layers[0], 'Layer: 0')
        self.assertEquals(layers[99], 'Layer: 99')

    def test_get_layers_returns_all_if_skipping_negitive(self, mock_AsynchronousGcodeReader):
        viewer = Viewer()
        test_file = 'test_file.gcode'
        mock_asynchronous_gcode_reader = mock_AsynchronousGcodeReader.return_value
        viewer.load_gcode(test_file)
        viewer_call_back = mock_AsynchronousGcodeReader.call_args_list[0][0][1]
        for i in range(0,100):
            viewer_call_back('Layer: %s' % i)
        complete_call_back = mock_AsynchronousGcodeReader.call_args_list[0][0][2]
        complete_call_back()

        layers = viewer.get_layers(50,60,-5)

        self.assertEquals(10,len(layers))
        self.assertEquals(layers[0], 'Layer: 50')
        self.assertEquals(layers[9], 'Layer: 59')

    def test_loading_a_new_file_removes_old_ones_layers(self, mock_AsynchronousGcodeReader):
        viewer = Viewer()
        test_file1 = 'test_file1.gcode'
        test_file2 = 'test_file2.gcode'
        mock_asynchronous_gcode_reader = mock_AsynchronousGcodeReader.return_value
        viewer.load_gcode(test_file1)
        viewer_call_back = mock_AsynchronousGcodeReader.call_args_list[0][0][1]
        for i in range(0,100):
            viewer_call_back('Old Layer: %s' % i)
        complete_call_back = mock_AsynchronousGcodeReader.call_args_list[0][0][2]
        complete_call_back()

        viewer.load_gcode(test_file2)
        viewer_call_back = mock_AsynchronousGcodeReader.call_args_list[0][0][1]
        for i in range(0,100):
            viewer_call_back('New Layer: %s' % i)
        complete_call_back = mock_AsynchronousGcodeReader.call_args_list[0][0][2]
        complete_call_back()

        layers = viewer.get_layers()

        self.assertEquals(100,len(layers))
        self.assertEquals(layers[0], 'New Layer: 0')

if __name__ == '__main__':
    unittest.main()
