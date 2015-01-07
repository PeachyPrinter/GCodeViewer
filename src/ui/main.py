import wx
import wx.lib.newevent
from api.viewer import Viewer
from gl import GCodeCanvas, GLProcesser
import logging

class DisplayPanel(wx.Panel):
    def __init__(self, parent):
        self.parent = parent
        wx.Panel.__init__(self, self.parent, -1, style=wx.RAISED_BORDER)
        
        logging.debug("Starting api")
        self.api = Viewer()
        self.status = ""
        self.UpdateEvent, EVT_UPDATE = wx.lib.newevent.NewEvent()
        self.Bind(EVT_UPDATE, self.updateDisplay)

        sizer_display_control = wx.BoxSizer(wx.VERTICAL)

        control_sizer = wx.FlexGridSizer(3,2,5,5)

        layer_slider_text = wx.StaticText(self, label="Centre Layer") 
        layers_to_display_slider_text = wx.StaticText(self, label="Number of Layers") 
        layer_parse_text = wx.StaticText(self, label="Layers to Hide") 

        self.layer_slider = wx.Slider(self, value = 1, minValue = 1, maxValue = 2)
        self.layers_slider = wx.Slider(self, value = 1, minValue = 1, maxValue = 2)
        self.skip_slider = wx.Slider(self, value = 50, minValue = 1, maxValue = 200)

        control_sizer.Add(layer_slider_text)
        control_sizer.Add(self.layer_slider,1,wx.EXPAND)

        control_sizer.Add(layers_to_display_slider_text)
        control_sizer.Add(self.layers_slider,1,wx.EXPAND)

        control_sizer.Add(layer_parse_text)
        control_sizer.Add(self.skip_slider,1,wx.EXPAND)

        control_sizer.AddGrowableCol(1, 1)

        sizer_display_control.Add(control_sizer,0,wx.EXPAND,5)
        logging.debug("Starting processor")
        self.processor = GLProcesser()
        logging.debug("Starting canvas")
        self.canvas = GCodeCanvas(self,self.processor)
        sizer_display_control.Add(self.canvas,1,wx.ALL|wx.EXPAND, 5)

        self.SetAutoLayout(True)
        self.SetSizer(sizer_display_control)
        self.SetFocus()

        self.Bind(wx.EVT_SLIDER, self.change_layer)

    def change_layer(self,event):
            bottom = self.layer_slider.GetValue() - self.layers_slider.GetValue() / 2
            top = self.layer_slider.GetValue() + self.layers_slider.GetValue() / 2
            skip = self.skip_slider.GetValue()
            logging.debug("Data Type: %s" % type(bottom) )
            self.processor.update(self.api.get_layers(bottom,top,skip))

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
        self.layer_slider.SetMax(message.data)
        self.layers_slider.SetMax(message.data)
        self.layer_slider.SetValue(message.data / 2)
        self.layers_slider.SetValue(message.data)
        self.change_layer(None)
        logging.info('Got Layers')

    def shutdown(self):
        pass
