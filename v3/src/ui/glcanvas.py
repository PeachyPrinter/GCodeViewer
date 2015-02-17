import wx
import logging
from wx import glcanvas
import OpenGL.GLUT as glut
import OpenGL.GL as gl


class GLCanvas(glcanvas.GLCanvas):

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
        gl.glViewport(0, 0, size.width, size.height)

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
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glFrustum(-0.5, 0.5, -0.1, 0.5, 0.5, 8.0)

        # position viewer
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glTranslatef(0.0, 0.0, -2.0)

        # position object
        gl.glRotatef(self.y, 1.0, 0.0, 0.0)
        gl.glRotatef(self.x, 0.0, 1.0, 0.0)

        gl.glEnable(gl.GL_DEPTH_TEST)
        # glEnable(GL_LIGHTING)
        glut.glutInit()
        # glEnable(GL_LIGHT0)
        self.DoSetViewport()

    def OnDraw(self):
        # clear color and depth buffers
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        # self.processor.updatenow()
        # index = self.processor.get_index()
        # if index:
        #     glCallList(index)
        glut.glutWireCube(1.0)

        if self.size is None:
            self.size = self.GetClientSize()
        w, h = self.size
        w = max(w, 1.0)
        h = max(h, 1.0)
        xScale = 180.0 / w
        yScale = 180.0 / h
        logging.debug("X:Y: %s:%s" % (self.xrot, self.yrot))

        # Vertical Rotation Revert
        gl.glTranslatef(0.0, 0.5, 0.0)
        gl.glRotatef(0.0 - (self.lastroty * yScale), 1.0, 0.0, 0.0)
        gl.glTranslatef(0.0, -0.5, 0.0)

        # Horizontal Rotation Revert
        gl.glRotatef(0.0 - (self.lastrotx * xScale), 0.0, 1.0, 0.0)

        # Scale Revert (Z pos)
        gl.glTranslatef(0.0, 0.0, 0.0 - self.last_scale)

        # Scale
        gl.glTranslatef(0.0, 0.0, 0.0 + self.scale)

        # Horizontal Rotation
        gl.glRotatef(self.xrot * xScale, 0.0, 1.0, 0.0)

        # Vertical Rotation
        gl.glTranslatef(0.0, 0.5, 0.0)
        gl.glRotatef(self.yrot * yScale, 1.0, 0.0, 0.0)
        gl.glTranslatef(0.0, -0.5, 0.0)

        self.last_scale = self.scale
        self.lastrotx, self.lastroty = self.xrot, self.yrot

        self.SwapBuffers()