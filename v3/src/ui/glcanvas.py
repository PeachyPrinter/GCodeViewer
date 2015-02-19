import wx
import os
import logging
import time
from wx import glcanvas
import numpy as np
import OpenGL.GL as gl

from infrastructure import jtutil
from infrastructure.jtgltext import JTGLText
from infrastructure.jtobjects import JTObjects


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
        self.zoom = 1.0
        self.xrot = self.lastrotx = 0.0
        self.yrot = self.lastroty = 0.0

        self.frames = 0
        self.fps_start = time.time()
        self.fps = 0.0
        self.dirty_p = True
        self.dirty_c = True

        self.projection_matrix = None
        self.camera_matrix = None

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)

    def InitGL(self):
        size = self.size = self.GetClientSize()
        self.text = JTGLText(os.path.join('resources'), size.width, size.height)
        self.jtobjects = JTObjects(os.path.join('resources'), self.get_projection_matrix, self.get_camera_matrix)
        self.DoSetViewport()

    def get_projection_matrix(self):
        if self.dirty_p or self.projection_matrix is None:
            near = 1.0
            far = 10.0
            left = -self.zoom
            right = self.zoom
            top = self.zoom
            bottom = -self.zoom

            fov_x = (2 * near) / (right - left)
            fov_y = (2 * near) / (top - bottom)
            fov_z = (-2 * far * near)/(far - near)

            tra_x = (right + left)/(right - left)
            tra_y = (top + bottom)/(top - bottom)
            tra_z = -(far + near) / (far - near)

            self.projection_matrix = np.swapaxes(np.matrix([[fov_x,    0.0,    tra_x,      0.0],
                                                [0.0,    fov_y,    tra_y,      0.0],
                                                [0.0,      0.0,    tra_z,    fov_z],
                                                [0.0,      0.0,     -1.0,      0.0]], dtype=np.float32),0,1)
            self.dirty_p = False
        return self.projection_matrix

    def get_camera_matrix(self):
        if self.dirty_c or self.camera_matrix is None:
            print("Getting movement x,y: %s,%s" % (self.xrot, -self.yrot))

            eye = np.array([self.xrot / 10.0, self.yrot / -10.0, -3.0])
            at = np.array([0.0, 0.0, 0.0])
            up = np.array([0.0, 1.0, 0.0])

            self.camera_matrix = jtutil.getLookAtMatrix(eye, at, up)

            # self.camera_matrix = np.matrix([[1.0,    0.0,    0.0,   0],
            #                                 [0.0,    1.0,    0.0,   0],
            #                                 [0.0,    0.0,    1.0,    0],
            #                                 [self.xrot / 10.0,    self.yrot / -10.0,    -3.0,     1.0]], dtype=np.float32)
            self.dirty_c = False
        return self.camera_matrix

    def OnEraseBackground(self, event):
        # Do nothing, to avoid flashing on MSW.
        pass

    def OnSize(self, event):
        wx.CallAfter(self.DoSetViewport)
        event.Skip()

    def DoSetViewport(self):
        size = self.size = self.GetClientSize()
        if self.init:
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
            self.zoom += 0.01
        else:
            self.zoom -= 0.01
        self.dirty = True
        logging.info("New Zoom: %s" % self.zoom)
        self.Refresh(False)

    def OnMouseMotion(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            self.lastx, self.lasty = self.x, self.y
            self.x = evt.GetPosition()[0]
            self.y = evt.GetPosition()[1]
            logging.debug('Diff X:Y:  %s:%s ' % (self.x - self.lastx, self.y - self.lasty))
            self.xrot += self.x - self.lastx
            self.yrot += self.y - self.lasty
            self.dirty_c = True
            self.dirty_p = True
            self.Refresh(False)

    def OnDraw(self):
        self.frames += 1
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        self.jtobjects.draw_grid()

        if self.frames % 100 == 0:
            self.fps = 100.0 / (time.time() - self.fps_start)
            self.fps_start = time.time()
        self.text.printgl('FPS: %s' % self.fps)

        self.SwapBuffers()