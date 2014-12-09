import wx
import wx.lib.newevent
from api.viewer import Viewer

class DisplayPanel(wx.Panel):
    def __init__(self, parent):
        self.parent = parent
        wx.Panel.__init__(self, self.parent, -1)
        self.api = Viewer()
        self.status = ""

        self.UpdateEvent, EVT_UPDATE = wx.lib.newevent.NewEvent()
        self.Bind(EVT_UPDATE, self.updateDisplay)

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