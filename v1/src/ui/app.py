import wx
from main import DisplayPanel

import logging

class GCodeViewerApp(wx.App):
    def __init__(self, path):
        logging.info('Starting Application')
        self.frame = None
        wx.App.__init__(self, redirect=False)
        logging.info("Started Application")
    
    def setup_menu(self):
        menuBar = wx.MenuBar()
        menu = wx.Menu()
        menu_open_item = menu.Append(-1, "&Open\tCtrl-O", "Open")
        menu_exit_item = menu.Append(wx.ID_EXIT, "E&xit\tCtrl-Q", "Exit")

        self.Bind(wx.EVT_MENU, self.OnOpen, menu_open_item)
        self.Bind(wx.EVT_MENU, self.OnExitApp, menu_exit_item)
        

        menuBar.Append(menu, "&File")
        self.frame.SetMenuBar(menuBar)

    def OnInit(self):
        logging.debug("Initting")
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
        sizer = wx.BoxSizer(wx.VERTICAL)
        logging.debug("Starting display panel")
        display_panel = DisplayPanel(self.frame)
        logging.debug("Display panel started")
        sizer.Add(display_panel,1,wx.EXPAND|wx.ALL)
        self.frame.SetSizer(sizer)
        logging.info("Display Size: %s,%s" % wx.DisplaySize())
        self.frame.SetSize(wx.DisplaySize())
        display_panel.SetFocus()
        self.window = display_panel
        frect = self.frame.GetRect()

        self.SetTopWindow(self.frame)
        return True

    def OnOpen(self, event):
        openFileDialog = wx.FileDialog(self.window, "Open GCODE file", "", "", "gcocde files (*.gcode)|*.gcode", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return     # the user changed idea...

        # proceed loading the file chosen by the user
        # this can be done with e.g. wxPython input streams:
        file_in_stream = open(openFileDialog.GetPath(), 'r')

        self.window.load_file(file_in_stream)

    def OnExitApp(self, evt):
        self.frame.Close(True)

    def OnCloseFrame(self, evt):
        if hasattr(self, "window") and hasattr(self.window, "shutdown"):
            self.window.shutdown()
        evt.Skip()