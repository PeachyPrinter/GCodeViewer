import wx
from wx import glcanvas
from OpenGL.GL import *
from OpenGL.GLUT import *
import logging


class Canvas(glcanvas.GLCanvas):

    def __init__(self, parent):
        glcanvas.GLCanvas.__init__(self, parent, -1)
        self.init = False
        self.context = glcanvas.GLContext(self)
        # initial mouse position
        self.lastx = self.x = 0
        self.lasty = self.y = 0
        self.size = None
        self.last_scale = 0.0
        self.scale = 0.0
        self.xrot = self.lastrotx = 0.0
        self.yrot = self.lastroty = 0.0
        self.display_list_id = None

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)

    def OnEraseBackground(self, event):
        # Do nothing, to avoid flashing on MSW.
        pass

    def OnSize(self, event):
        wx.CallAfter(self.DoSetViewport)
        event.Skip()

    def DoSetViewport(self):
        size = self.size = self.GetClientSize()
        self.SetCurrent(self.context)
        glViewport(0, 0, size.width, size.height)

    def OnPaint(self, event):
        # dc = wx.PaintDC(self)
        self.SetCurrent(self.context)
        if not self.init:
            self.InitGL()
            self.init = True
        self.OnDraw()

    def OnMouseDown(self, evt):
        self.CaptureMouse()
        self.x, self.y = evt.GetPosition()

    def OnMouseUp(self, evt):
        self.ReleaseMouse()

    def OnMouseWheel(self, evt):
        if evt.GetWheelRotation() > 0:
            self.scale += 0.01
        else:
            self.scale -= 0.01
        logging.info("New Scale: %s" % self.scale)
        self.Refresh(False)

    def OnMouseMotion(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            self.lastx, self.lasty = self.x, self.y
            self.x = evt.GetPosition()[0]
            self.y = evt.GetPosition()[1]
            logging.debug('Diff X:Y:  %s:%s ' % (self.x - self.lastx, self.y - self.lasty))
            self.xrot += self.x - self.lastx
            self.yrot += self.y - self.lasty
            self.Refresh(False)

    def InitGL(self):
        # set viewing projection
        glMatrixMode(GL_PROJECTION)
        glFrustum(-0.5, 0.5, -0.1, 0.5, 0.5, 8.0)

        # position viewer
        glMatrixMode(GL_MODELVIEW)
        glTranslatef(0.0, 0.0, -2.0)

        # position object
        glRotatef(self.y, 1.0, 0.0, 0.0)
        glRotatef(self.x, 0.0, 1.0, 0.0)

        glEnable(GL_DEPTH_TEST)
        # glEnable(GL_LIGHTING)

        glutInit()

        self.display_list_id = glGenLists(1)
        glNewList(self.display_list_id, GL_COMPILE)
        glutWireCube(1.0)
        glEndList()

        # glEnable(GL_LIGHT0)
        self.DoSetViewport()

    def OnDraw(self):
        # clear color and depth buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # self.processor.updatenow()
        # index = self.processor.get_index()
        # if index:
        if self.display_list_id:
            glCallList(self.display_list_id)

        if self.size is None:
            self.size = self.GetClientSize()
        w, h = self.size
        w = max(w, 1.0)
        h = max(h, 1.0)
        xScale = 180.0 / w
        yScale = 180.0 / h
        logging.debug("X:Y: %s:%s" % (self.xrot, self.yrot))

        # Vertical Rotation Revert
        glTranslatef(0.0, 0.5, 0.0)
        glRotatef(0.0 - (self.lastroty * yScale), 1.0, 0.0, 0.0)
        glTranslatef(0.0, -0.5, 0.0)

        # Horizontal Rotation Revert
        glRotatef(0.0 - (self.lastrotx * xScale), 0.0, 1.0, 0.0)

        # Scale Revert (Z pos)
        glTranslatef(0.0, 0.0, 0.0 - self.last_scale)

        # Scale
        glTranslatef(0.0, 0.0, 0.0 + self.scale)

        # Horizontal Rotation
        glRotatef(self.xrot * xScale, 0.0, 1.0, 0.0)

        # Vertical Rotation
        glTranslatef(0.0, 0.5, 0.0)
        glRotatef(self.yrot * yScale, 1.0, 0.0, 0.0)
        glTranslatef(0.0, -0.5, 0.0)

        self.last_scale = self.scale
        self.lastrotx, self.lastroty = self.xrot, self.yrot

        self.SwapBuffers()
