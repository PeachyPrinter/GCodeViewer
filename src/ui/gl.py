import wx
from wx import glcanvas
from OpenGL.GL import *
from OpenGL.GLUT import *
import threading
import time
import logging
from domain.commands import *

class GCodeCanvas(glcanvas.GLCanvas):

    def __init__(self, parent, processor):
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
           self.scale += 0.01
        else:
            self.scale -= 0.01
        
        logging.info("New Scale: %s" % self.scale)
        self.Refresh(False)

    def OnMouseMotion(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            self.lastx,self.lasty = self.x,self.y
            self.x = evt.GetPosition()[0] 
            self.y = evt.GetPosition()[1]
            logging.info('Diff X:Y:  %s:%s '% (self.x - self.lastx, self.y - self.lasty))
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
        # glEnable(GL_LIGHT0)

    def OnDraw(self):
        # clear color and depth buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # draw six faces of a cube
        self.processor.updatenow()
        index = self.processor.get_index()
        if index:
            glCallList(index)

        if self.size is None:
            self.size = self.GetClientSize()
        w, h = self.size
        w = max(w, 1.0)
        h = max(h, 1.0)
        xScale = 180.0 / w
        yScale = 180.0 / h
        logging.info("X:Y: %s:%s" % (self.xrot,self.yrot))

        glRotatef(0.0 - (self.lastroty * yScale), 1.0, 0.0, 0.0);
        glRotatef(0.0 - (self.lastrotx * xScale), 0.0, 1.0, 0.0);
        glTranslatef(0.0,0.0,0.0 - self.last_scale)

        glTranslatef(0.0, 0.0, 0.0 + self.scale)
        glRotatef(self.xrot * xScale, 0.0, 1.0, 0.0);
        glRotatef(self.yrot * yScale, 1.0, 0.0, 0.0);


        
        self.last_scale = self.scale
        self.lastrotx, self.lastroty = self.xrot, self.yrot


        self.SwapBuffers()


class GLProcesser():
    def __init__(self):
        self.currentDisplayList = glGenLists(1);
        glNewList(self.currentDisplayList, GL_COMPILE)
        glEndList()
        self.updateRequired = False
        self.layers = []
        self.movecolour = [1.0,0.0,0.0]
        self.drawcolour = [0.0,1.0,0.0]

    def get_index(self):
        return self.currentDisplayList

    def update(self, layers):
        logging.info("Update Requested")
        self.layers = layers
        self.updateRequired = True

    def updatenow(self):
        if self.updateRequired:
            logging.info("Required Update")
            self._populate_layers()
            self.updateRequired = False

    def _populate_layers(self):
        logging.info("Started Adding Display List")
        self.nextDisplayList = glGenLists(1);
        glNewList(self.nextDisplayList, GL_COMPILE)
        glBegin(GL_QUADS)
        layer_count = len(self.layers)
        layer_height = (self.layers[layer_count -1].z - self.layers[0].z ) / layer_count
        logging.info("Layer Height: %s" % layer_height)
        self.base_scale = 1.0 / self.layers[layer_count -1].z
        current_scale = self.base_scale
        logging.info("Base Scale: %s" % self.base_scale)
        for layer in self.layers:
            for command in layer.commands:
                if type(command) == LateralDraw:
                    glColor3fv(self.drawcolour)
                else:
                    glColor3fv(self.movecolour)
                glVertex3f(command.start[0] * current_scale,   layer.z * current_scale,                                    command.start[1] * current_scale)
                glVertex3f(command.start[0] * current_scale,   layer.z * current_scale+layer_height*current_scale        , command.start[1] * current_scale)
                glVertex3f(command.end[0]   * current_scale,   layer.z * current_scale+layer_height*current_scale        , command.end[1]   * current_scale)
                glVertex3f(command.end[0]   * current_scale,   layer.z * current_scale,                                    command.end[1]   * current_scale)

        glEnd()
        glEndList()
        old = self.currentDisplayList
        self.currentDisplayList = self.nextDisplayList
        glDeleteLists(old, 1)
        
        logging.info("Finished Adding Display List")






