from infrastructure.asynchronous_gcode_reader import AsynchronousGcodeReader 

class Viewer(object):
    def __init__(self):
        pass

    def load_gcode(self, afile, call_back = None):
        AsynchronousGcodeReader(afile,self.load_gcode_call_back,self.load_gcode_complete).start()

    def get_layers(self,start,end,skip):
        pass

    def load_gcode_call_back(self):
        pass

    def load_gcode_complete(self):
        pass