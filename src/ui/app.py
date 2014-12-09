class GCodeViewerApp(wx.App):
    def __init__(self, path):
        self.api = ViewerAPI(gcode_file)
        wx.App.__init__(self, redirect=False)
        

    def OnInit(self):
        frame = wx.Frame(None, 
            id = -1, 
            title = "Peachy GCode Viewer", 
            pos=(0,0),
            style=wx.DEFAULT_FRAME_STYLE, 
            )

        frame.CreateStatusBar()

        menuBar = wx.MenuBar()
        menu = wx.Menu()
        item = menu.Append(wx.ID_EXIT, "E&xit\tCtrl-Q", "Exit demo")
        self.Bind(wx.EVT_MENU, self.OnExitApp, item)
        menuBar.Append(menu, "&File")
        
        frame.SetMenuBar(menuBar)
        frame.Show(True)
        frame.Bind(wx.EVT_CLOSE, self.OnCloseFrame)

        display_panel = DisplayPanel(frame, self.api)

        frame.SetSize(wx.DisplaySize())
        display_panel.SetFocus()
        self.window = display_panel
        frect = frame.GetRect()

        self.SetTopWindow(frame)
        self.frame = frame
        return True

    def OnExitApp(self, evt):
        self.frame.Close(True)

    def OnCloseFrame(self, evt):
        if hasattr(self, "window") and hasattr(self.window, "ShutdownDemo"):
            self.window.ShutdownDemo()
        evt.Skip()