import wx
import wx.lib.newevent
from api.viewer import Viewer

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
        sizer_display_control.Add(control_sizer,0,wx.EXPAND|wx.ALL,5)

        layer_slider_text = wx.StaticText(parent, id=-1, label="Centre Layer") 
        layers_to_display_slider_text = wx.StaticText(parent, id=-1, label="Number of Layer") 
        layer_parse_text = wx.StaticText(parent, id=-1, label="Layers to Hide") 

        layer_slider = wx.Slider(self, value = 1, minValue = 1, maxValue = 2)
        layers_slider = wx.Slider(self, value = 1, minValue = 1, maxValue = 2)
        skip_slider = wx.Slider(self, value = 50, minValue = 1, maxValue = 50)

        control_sizer.Add(layer_slider_text)
        control_sizer.Add(layer_slider,0,wx.EXPAND|wx.ALL)

        control_sizer.Add(layers_to_display_slider_text)
        control_sizer.Add(layers_slider,0,wx.EXPAND|wx.ALL)

        control_sizer.Add(layer_parse_text)
        control_sizer.Add(skip_slider,0,wx.EXPAND|wx.ALL)

        control_sizer.AddGrowableCol(1, 1)

        self.SetAutoLayout(True)
        self.SetSizer(control_sizer)
        self.SetFocus()

    def load_file(self, afile):
        self.status = "Loading"
        self.api.load_gcode(afile, self._gcode_load_call_back,self._gcode_complete_call_back)

    def _gcode_load_call_back(self,layers):
        if layers % 10 == 0:
            wx.PostEvent(self, self.UpdateEvent(data = layers))

    def _gcode_complete_call_back(self,layers):
        self.status = "Complete"
        wx.PostEvent(self, self.UpdateEvent(data = layers))

    def updateDisplay(self,message):
        self.parent.SetStatusText("%s : %s Layers" % (self.status,message.data))