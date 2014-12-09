import wx
from api.viewer import Viewer
from main import DisplayPanel

class GCodeViewerApp(wx.App):
    def __init__(self, path):
        self.api = Viewer()
        self.frame = None
        wx.App.__init__(self, redirect=False)
    
    def setup_menu(self):
        menuBar = wx.MenuBar()
        menu = wx.Menu()
        menu_exit_item = menu.Append(wx.ID_EXIT, "E&xit\tCtrl-Q", "Exit")
        self.Bind(wx.EVT_MENU, self.OnExitApp, menu_exit_item)
        menu_open_item = menu.Append(wx.ID_EXIT, "&Open\tCtrl-O", "Open")
        self.Bind(wx.EVT_MENU, self.OnOpen, menu_open_item)
        menuBar.Append(menu, "&File")
        self.frame.SetMenuBar(menuBar)

    def OnInit(self):
        self.frame = wx.Frame(None, 
            id = -1, 
            title = "Peachy GCode Viewer", 
            pos=(0,0),
            style=wx.DEFAULT_FRAME_STYLE, 
            )

        self.frame.CreateStatusBar()
        self.setup_menu()
        
        self.frame.Show(True)
        self.frame.Bind(wx.EVT_CLOSE, self.OnCloseFrame)

        display_panel = DisplayPanel(self.frame, self.api)

        self.frame.SetSize(wx.DisplaySize())
        display_panel.SetFocus()
        self.window = display_panel
        # frect = self.frame.GetRect()

        self.SetTopWindow(self.frame)
        return True

    def OnOpen(self, event):
        openFileDialog = wx.FileDialog(self.window, "Open XYZ file", "", "", "XYZ files (*.xyz)|*.xyz", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return     # the user changed idea...

        # proceed loading the file chosen by the user
        # this can be done with e.g. wxPython input streams:
        input_stream = wx.FileInputStream(openFileDialog.GetPath())

        if not input_stream.IsOk():
            wx.LogError("Cannot open file '%s'."%openFileDialog.GetPath())
            return

    def OnExitApp(self, evt):
        self.frame.Close(True)

    def OnCloseFrame(self, evt):
        if hasattr(self, "window") and hasattr(self.window, "shutdown"):
            self.window.shutdown()
        evt.Skip()