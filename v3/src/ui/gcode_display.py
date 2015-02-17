import wx
import wx.lib.newevent

from glcanvas import GLCanvas
import logging


class GcodeDisplayPanel(wx.Panel):
    def __init__(self, parent):
        self.parent = parent
        wx.Panel.__init__(self, self.parent, -1, style=wx.RAISED_BORDER)
        logging.debug("Starting api")
        self.status = ""
        self.UpdateEvent, EVT_UPDATE = wx.lib.newevent.NewEvent()
        self.Bind(EVT_UPDATE, self.updateDisplay)
        sizer_display_control = wx.BoxSizer(wx.HORIZONTAL)
        self.skip_slider = wx.Slider(self, value=50, minValue=1, maxValue=200)
        sizer_display_control.Add(self.skip_slider, 1, wx.ALL | wx.EXPAND, 5)
        self.canvas = GLCanvas(self)
        sizer_display_control.Add(self.canvas, 1, wx.ALL | wx.EXPAND, 5)

        self.SetAutoLayout(True)
        self.SetSizer(sizer_display_control)
        self.SetFocus()

    def load_file(self, afile):
        self.status = "Loading"
        logging.info("Loading file")
        self.api.load_gcode(afile, self._gcode_load_call_back, self._gcode_complete_call_back)

    def updateDisplay(self, message):
        logging.info('Updating display')

    def shutdown(self):
        pass
