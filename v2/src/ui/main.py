import wx
import wx.lib.newevent
from gl import Canvas
import logging
from api.points_loader import Loader


class DisplayPanel(wx.Panel):
    def __init__(self, parent):
        self.parent = parent
        wx.Panel.__init__(self, self.parent, -1, style=wx.RAISED_BORDER)
        logging.debug("Starting api")
        self.status = ""
        self.UpdateEvent, EVT_UPDATE = wx.lib.newevent.NewEvent()
        self.Bind(EVT_UPDATE, self.updateDisplay)
        sizer_display_control = wx.BoxSizer(wx.VERTICAL)
        control_sizer = wx.FlexGridSizer(3, 2, 5, 5)
        layer_parse_text = wx.StaticText(self, label="Layers to Hide")
        self.skip_slider = wx.Slider(self, value=50, minValue=1, maxValue=200)

        control_sizer.Add(layer_parse_text)
        control_sizer.Add(self.skip_slider, 1, wx.EXPAND)

        control_sizer.AddGrowableCol(1, 1)

        sizer_display_control.Add(control_sizer, 0, wx.EXPAND, 5)

        self.canvas = Canvas(self)
        sizer_display_control.Add(self.canvas, 1, wx.ALL | wx.EXPAND, 5)

        self.SetAutoLayout(True)
        self.SetSizer(sizer_display_control)
        self.SetFocus()

        self.Bind(wx.EVT_SLIDER, self.change_layer)

    def load_folder(self, folder):
        self.status = "Loading"
        logging.info("Loading file")
        self.canvas.display_list_id = self.api.displayListFromWaves(folder)

    def _gcode_load_call_back(self, layers):
        if layers % 10 == 0:
            logging.info('Posting GCODE Processing Update')
            wx.PostEvent(self, self.UpdateEvent(data=layers))

    def _gcode_complete_call_back(self, layers):
        self.status = "Complete"
        logging.info('Posting GCODE Complete Update')
        wx.PostEvent(self, self.UpdateEvent(dat=layers))

    def updateDisplay(self, message):
        logging.info('Updating display')
        self.parent.SetStatusText("%s : %s Layers" % (self.status, message.data))
        logging.info('Getting Layers')
        self.layer_slider.SetMax(message.data)
        self.layers_slider.SetMax(message.data)
        self.layer_slider.SetValue(message.data / 2)
        self.layers_slider.SetValue(message.data)
        self.change_layer(None)
        logging.info('Got Layers')

    def shutdown(self):
        pass
