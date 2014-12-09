import wx
from wx import glcanvas
from OpenGL.GL import *
from OpenGL.GLUT import *
import threading
import time
import logging

class GCodeCanvas(glcanvas.GLCanvas):

    def __init__(self, parent, processor):
        glcanvas.GLCanvas.__init__(self, parent, -1)
        self.init = False
        self.context = glcanvas.GLContext(self)
        # initial mouse position
        self.lastx = self.x = 30
        self.lasty = self.y = 30
        self.z = 0.0
        self.size = None
        self.scale = 0.001

        self.processor = processor

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
        self.DoSetViewport()

    def OnEraseBackground(self, event):
        pass # Do nothing, to avoid flashing on MSW.

    def OnSize(self, event):
        wx.CallAfter(self.DoSetViewport)
        event.Skip()

    def DoSetViewport(self):
        size = self.size = self.GetClientSize()
        self.SetCurrent(self.context)
        glViewport(0, 0, size.width, size.height)
        
    def OnPaint(self, event):
        dc = wx.PaintDC(self)
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
            self.scale += 0.0001
        else:
            self.scale -= 0.0001
        self.Refresh(False)

    def OnMouseMotion(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            self.lastx, self.lasty = self.x, self.y
            self.x, self.y = evt.GetPosition()
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
        # glEnable(GL_LIGHT0)

    def OnDraw(self):
        # clear color and depth buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # draw six faces of a cube
        # index = self.processor.get_index()
        # if index:
        #     glCallList(index)

        if self.size is None:
            self.size = self.GetClientSize()
        w, h = self.size
        w = max(w, 1.0)
        h = max(h, 1.0)
        xScale = 180.0 / w
        yScale = 180.0 / h
        # glRotatef((self.y - self.lasty) * yScale, 1.0, 0.0, 0.0);
        glRotatef((self.x - self.lastx) * xScale, 0.0, 1.0, 0.0);

        # glTranslatef(0.0, 0.0, self.z)
        self.z = 0.0

        self.SwapBuffers()


class GLProcesser(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.currentDisplayList = None
        self.updateRequired = False
        self.running = False
        self.layers = []
        self.scale = 0.0001

    def get_index(self):
        return self.currentDisplayList

    def update(self, layers):
        logging.info("Update Requested")
        self.layers = layers
        self.updateRequired = True

    def run(self):
        self.running = True
        while self.running:
            if self.updateRequired:
                logging.info("Required Update")
                self._populate_layers()
                self.updateRequired = False
            else:
                time.sleep(1)

    def _populate_layers(self):
        logging.info("Started Adding Display List")
        self.nextDisplayList = glGenLists(1);
        glNewList(self.nextDisplayList, GL_COMPILE);
        glBegin(GL_QUADS)
        for layer in layers:
            for command in layer.commands:
                if type(command) == LateralDraw:
                    glColor3fv(drawcolour)
                else:
                    glColor3fv(movecolour)
                glVertex3f(command.start[0] * self.scale,   layer.z * self.scale,                command.start[1] * self.scale)
                glVertex3f(command.start[0] * self.scale,   layer.z * self.scale+self.scale*2.0, command.start[1] * self.scale)
                glVertex3f(command.end[0]   * self.scale,   layer.z * self.scale+self.scale*2.0, command.end[1]   * self.scale)
                glVertex3f(command.end[0]   * self.scale,   layer.z * self.scale,                command.end[1]   * self.scale)

        glEnd()
        glEndList();
        old = self.currentDisplayList
        self.currentDisplayList = self.nextDisplayList
        glDeleteLists(old, 1)
        
        logging.info("Finished Adding Display List")

    def close(self):
        self.running = False






