from infrastructure.asynchronous_gcode_reader import AsynchronousGcodeReader 

class Viewer(object):
    def __init__(self):
        self.layers = []
        self.current_layer_call_back = None
        self.current_complete_call_back = None

    def load_gcode(self, afile,layer_count_call_back = None, complete_call_back = None):
        self.current_layer_call_back = layer_count_call_back
        self.current_complete_call_back = complete_call_back
        AsynchronousGcodeReader(afile,self._load_gcode_call_back,self._load_gcode_complete).start()

    def get_layers(self,start,end,skip):
        pass

    def _load_gcode_call_back(self, layer):
        self.layers.append(layer)
        if self.current_layer_call_back:
            self.current_layer_call_back(len(self.layers))

    def _load_gcode_complete(self):
        if self.current_complete_call_back:
            self.current_complete_call_back(len(self.layers))