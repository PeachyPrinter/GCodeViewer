import wx
import logging
from gcode_display import GcodeDisplayPanel


class App(wx.App):
    def __init__(self, path):
        logging.info('Starting Application')
        self.frame = None
        wx.App.__init__(self, redirect=False)
        logging.info("Started Application")

    def setup_menu(self):
        menuBar = wx.MenuBar()
        menu = wx.Menu()
        menu_open_item = menu.Append(-1, "&Open File\tCtrl-O", "Open File")
        menu_exit_item = menu.Append(wx.ID_EXIT, "E&xit\tCtrl-Q", "Exit")

        self.Bind(wx.EVT_MENU, self.OnOpen, menu_open_item)
        self.Bind(wx.EVT_MENU, self.OnExitApp, menu_exit_item)

        menuBar.Append(menu, "&File")
        self.frame.SetMenuBar(menuBar)

    def OnInit(self):
        logging.debug("Initting")
        self.frame = wx.Frame(None,
                              id=-1,
                              title="Peachy Audio Viewer",
                              pos=(0, 0),
                              style=wx.DEFAULT_FRAME_STYLE,
                              )

        self.frame.CreateStatusBar()
        self.setup_menu()
        self.frame.Show(True)
        self.frame.Bind(wx.EVT_CLOSE, self.OnCloseFrame)
        sizer = wx.BoxSizer(wx.VERTICAL)
        logging.debug("Starting display panel")
        display_panel = GcodeDisplayPanel(self.frame)
        logging.debug("Display panel started")
        sizer.Add(display_panel, 1, wx.EXPAND | wx.ALL)
        self.frame.SetSizer(sizer)
        logging.info("Display Size: %s,%s" % wx.DisplaySize())
        self.frame.SetSize(wx.DisplaySize())
        display_panel.SetFocus()
        self.window = display_panel
        self.SetTopWindow(self.frame)
        return True

    def OnOpen(self, event):
        pass

    def OnExitApp(self, evt):
        self.frame.Close(True)

    def OnCloseFrame(self, evt):
        if hasattr(self, "window") and hasattr(self.window, "shutdown"):
            self.window.shutdown()
        evt.Skip()
