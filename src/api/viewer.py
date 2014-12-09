from infrastructure.asynchronous_gcode_reader import AsynchronousGcodeReader 

class Viewer(object):
    def __init__(self):
        self.layers = []

    def load_gcode(self, afile,layer_count_call_back = None):
        AsynchronousGcodeReader(afile,self.load_gcode_call_back,self.load_gcode_complete).start()

    def get_layers(self,start,end,skip):
        pass

    def load_gcode_call_back(self, layer):
        self.layers.append(layer)

    def load_gcode_complete(self):
        pass