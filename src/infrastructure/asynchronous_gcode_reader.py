import threading 

from gcode_layer_generator import GCodeReader

class AsynchronousGcodeReader(threading.Thread):
    def __init__(self, afile, call_back, complete):
        threading.Thread.__init__(self)
        self.afile = afile
        self.call_back = call_back
        self.complete = complete

    def run(self):
        print('here')
        self.complete()
        print('again')
