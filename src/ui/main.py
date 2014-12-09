import wx

class DisplayPanel(wx.Panel):
    def __init__(self, parent, api):
        self.parent = parent
        wx.Panel.__init__(self, self.parent, -1)