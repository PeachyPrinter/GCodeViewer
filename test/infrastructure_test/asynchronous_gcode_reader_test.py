import unittest
import sys
import time
import os
from mock import patch, Mock

sys.path.insert(0,os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0,os.path.join(os.path.dirname(__file__), '..', '..','src'))

from infrastructure.asynchronous_gcode_reader import AsynchronousGcodeReader
from domain.commands import *

@patch('infrastructure.asynchronous_gcode_reader.GCodeReader')
class AsynchronousGcodeReaderTest(unittest.TestCase):
    def test_calls_back_with_each_layer_and_complete(self, mock_GcodeReader):
        l1 = Layer(0.0,commands = [LateralDraw((1.0,1.0),(2.0,2.0),200.0)])
        l2 = Layer(0.1,commands = [LateralDraw((2.0,2.0),(1.5,1.5),200.0)])
        mock_gcode_reader = mock_GcodeReader.return_value
        mock_gcode_reader.get_layers.return_value = iter([l1,l2])
        call_backs = []
        complete = [False]
        tries = 0

        def test_callback(layer):
            call_backs.append(layer)

        def test_complete():
            complete[0] = True
        
        AsynchronousGcodeReader('file',test_callback,test_complete).start()

        while (not complete[0] and tries < 10):
            tries +=1
            time.sleep(0.1)

        self.assertTrue(tries < 10)
        self.assertEqual(2,len(call_backs))

 
if __name__ == '__main__':
    unittest.main()