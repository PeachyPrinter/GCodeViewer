import wx
import os
import logging
import time
from wx import glcanvas
import OpenGL.GLUT as glut
import OpenGL.GL as gl
from infrastructure.jtgltext import JTGLText


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

        self.frames = 0
        self.fps_start = time.time()
        self.fps = 0.0

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
        self.text.viewPortChanged(size.width, size.height)
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
        size = self.size = self.GetClientSize()
        self.text = JTGLText(os.path.join('resources'), size.width, size.height)
        self.DoSetViewport()

    def OnDraw(self):
        self.frames += 1
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        if self.frames % 100 == 0:
            self.fps = 100.0 / (time.time() - self.fps_start)
            self.fps_start = time.time()
        self.text.printgl('FPS: %s' % self.fps)

        self.SwapBuffers()