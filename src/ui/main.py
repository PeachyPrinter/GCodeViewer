import wx
import wx.lib.newevent
from api.viewer import Viewer
from gl import GCodeCanvas, GLProcesser
import logging

class DisplayPanel(wx.Panel):
    def __init__(self, parent):
        self.parent = parent
        wx.Panel.__init__(self, self.parent, -1, style=wx.RAISED_BORDER)
        
        
        self.api = Viewer()
        self.status = ""
        self.UpdateEvent, EVT_UPDATE = wx.lib.newevent.NewEvent()
        self.Bind(EVT_UPDATE, self.updateDisplay)

        sizer_display_control = wx.BoxSizer(wx.VERTICAL)

        control_sizer = wx.FlexGridSizer(3,2,5,5)

        layer_slider_text = wx.StaticText(self, label="Centre Layer") 
        layers_to_display_slider_text = wx.StaticText(self, label="Number of Layers") 
        layer_parse_text = wx.StaticText(self, label="Layers to Hide") 

        layer_slider = wx.Slider(self, value = 1, minValue = 1, maxValue = 2)
        layers_slider = wx.Slider(self, value = 1, minValue = 1, maxValue = 2)
        skip_slider = wx.Slider(self, value = 50, minValue = 1, maxValue = 50)

        control_sizer.Add(layer_slider_text)
        control_sizer.Add(layer_slider,1,wx.EXPAND)

        control_sizer.Add(layers_to_display_slider_text)
        control_sizer.Add(layers_slider,1,wx.EXPAND)

        control_sizer.Add(layer_parse_text)
        control_sizer.Add(skip_slider,1,wx.EXPAND)

        control_sizer.AddGrowableCol(1, 1)

        sizer_display_control.Add(control_sizer,0,wx.EXPAND,5)
        self.processor = GLProcesser()
        self.processor.start()
        self.canvas = GCodeCanvas(self,self.processor)
        sizer_display_control.Add(self.canvas,1,wx.ALL|wx.EXPAND, 5)

        self.SetAutoLayout(True)
        self.SetSizer(sizer_display_control)
        self.SetFocus()

    def load_file(self, afile):
        self.status = "Loading"
        logging.info("Loading file")
        self.api.load_gcode(afile, self._gcode_load_call_back,self._gcode_complete_call_back)

    def _gcode_load_call_back(self,layers):
        if layers % 10 == 0:
            logging.info('Posting GCODE Processing Update')
            wx.PostEvent(self, self.UpdateEvent(data = layers))

    def _gcode_complete_call_back(self,layers):
        self.status = "Complete"
        logging.info('Posting GCODE Complete Update')
        wx.PostEvent(self, self.UpdateEvent(data = layers))

    def updateDisplay(self,message):
        logging.info('Updating display')
        self.parent.SetStatusText("%s : %s Layers" % (self.status,message.data))
        logging.info('Getting Layers')
        self.processor.update(self.api.get_layers())
        logging.info('Got Layers')

    def shutdown(self):
        self.processor.close()
