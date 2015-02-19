import OpenGL.GL as gl
import numpy as np
import os
import ctypes
import time

from shader_loader import ShaderLoader
from numpy_gcode_reader import NumpyGcodeReader


class JTObjects(object):
    def __init__(self, resource_path, projection_matrix_function, camera_matrix_function):
        self.resource_path = resource_path
        self.projection_matrix_function = projection_matrix_function
        self.camera_matrix_function = camera_matrix_function
        self.load_shader_programs()
        self.init_grid()
        self.init_gcode_object()

    def load_shader_programs(self,):
        vertex_shader_file = os.path.join(self.resource_path, 'shaders', 'jt_object_vertex.glsl')
        fragment_shader_file = os.path.join(self.resource_path, 'shaders', 'jt_object_fragment.glsl')
        self.simple_object_shader = ShaderLoader.load_shaders(vertex_shader_file,fragment_shader_file)

    def init_grid(self,):
        self.grid_vao = gl.glGenVertexArrays(1)
        self.grid_vbo = gl.glGenBuffers(1)
        gl.glBindVertexArray(self.grid_vao)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.grid_vbo)

        posisitions = np.array([
                                     1.0,    0.0,    -1.0,    1.0,
                                     1.0,    0.0,     1.0,    1.0,
                                    -1.0,    0.0,     1.0,    1.0,
                                    -1.0,    0.0,     1.0,    1.0,
                                    -1.0,    0.0,    -1.0,    1.0,
                                     1.0,    0.0,    -1.0,    1.0,

                                    -1.0,    0.0,     0.0,    1.0,
                                     1.0,    0.0,     0.0,    1.0,
                                     1.0,     1.0,     0.0,    1.0,
                                     1.0,     1.0,     0.0,    1.0,
                                    -1.0,     1.0,     0.0,    1.0,
                                    -1.0,    0.0,     0.0,    1.0,

                                     0.0,    0.0,    -1.0,    1.0,
                                     0.0,     1.0,    -1.0,    1.0,
                                     0.0,     1.0,     1.0,    1.0,
                                     0.0,     1.0,     1.0,    1.0,
                                     0.0,    0.0,     1.0,    1.0,
                                     0.0,    0.0,    -1.0,    1.0,
                                    ], dtype=np.float32)

        colors = np.array(     [    1.0,    0.0,   0.0,    0.2,
                                    1.0,    0.0,   0.0,    0.2,
                                    1.0,    0.0,   0.0,    0.2,
                                    1.0,    0.0,   0.0,    0.2,
                                    1.0,    0.0,   0.0,    0.2,
                                    1.0,    0.0,   0.0,    0.2,

                                    0.0,    0.0,   1.0,    0.2,
                                    0.0,    0.0,   1.0,    0.2,
                                    0.0,    0.0,   1.0,    0.2,
                                    0.0,    0.0,   1.0,    0.2,
                                    0.0,    0.0,   1.0,    0.2,
                                    0.0,    0.0,   1.0,    0.2,

                                    0.0,    1.0,   0.0,    0.2,
                                    0.0,    1.0,   0.0,    0.2,
                                    0.0,    1.0,   0.0,    0.2,
                                    0.0,    1.0,   0.0,    0.2,
                                    0.0,    1.0,   0.0,    0.2,
                                    0.0,    1.0,   0.0,    0.2,
                                    ], dtype=np.float32)

        gl.glBufferData(gl.GL_ARRAY_BUFFER, (posisitions.size + colors.size) * 4, None, gl.GL_STATIC_DRAW)
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, 0, posisitions)
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, posisitions.size * 4, colors)
        self.grid_size = posisitions.size

    def draw_grid(self,):
        gl.glUseProgram(self.simple_object_shader)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glDepthFunc(gl.GL_LESS)

        gl.glBindVertexArray(self.grid_vao)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.grid_vbo)

        vProjection = gl.glGetUniformLocation(self.simple_object_shader, 'vProjection')
        vPosisition = gl.glGetAttribLocation(self.simple_object_shader, "vPosisition")
        vColor = gl.glGetAttribLocation(self.simple_object_shader, "vColor")
        vCamera = gl.glGetUniformLocation(self.simple_object_shader, 'vCamera')

        gl.glUniformMatrix4fv(vProjection, 1, gl.GL_FALSE, self.projection_matrix_function())
        gl.glUniformMatrix4fv(vCamera, 1, gl.GL_FALSE, self.camera_matrix_function())

        gl.glEnableVertexAttribArray(vPosisition)
        gl.glEnableVertexAttribArray(vColor)

        gl.glVertexAttribPointer(vPosisition, 4, gl.GL_FLOAT, gl.GL_FALSE, 0, None)
        gl.glVertexAttribPointer(vColor, 4, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(self.grid_size * 4))

        gl.glDrawArrays(gl.GL_TRIANGLES, 0, self.grid_size / 4)

    def init_gcode_object(self,):
        self.gcode_vao = gl.glGenVertexArrays(1)
        self.gcode_vbo = gl.glGenBuffers(1)
        # gl.glBindVertexArray(self.gcode_vao)
        # gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.gcode_vbo)

        file_handle = open('julia.gcode', 'r')
        self.npgcr = NumpyGcodeReader(file_handle)
        self.npgcr.start()
        self._last_updateTime = 0.0
        self.gcode_done = False

    def refresh_gcode_object(self,):
        if not self.gcode_done and time.time() - self._last_updateTime >= 4.0:
            gl.glBindVertexArray(self.gcode_vao)
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.gcode_vbo)

            status, pos, col = self.npgcr.get_current()
            if status is "Complete":
                self.gcode_done = True
            posisitions = np.array(pos, dtype=np.float32)
            scale = 1.0 / np.amax(posisitions)
            scale = np.array([scale, scale, scale, 1.0], dtype=np.float32)
            posisitions = posisitions * scale
            colors = np.array(col, dtype=np.float32)

            gl.glBufferData(gl.GL_ARRAY_BUFFER, (posisitions.size + colors.size) * 4, None, gl.GL_STATIC_DRAW)
            gl.glBufferSubData(gl.GL_ARRAY_BUFFER, 0, posisitions)
            gl.glBufferSubData(gl.GL_ARRAY_BUFFER, posisitions.size * 4, colors)
            self.gcode_size = posisitions.size
            self._last_updateTime = time.time()

    def draw_gcode_object(self,):
        self.refresh_gcode_object()
        gl.glUseProgram(self.simple_object_shader)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glDepthFunc(gl.GL_LESS)

        gl.glBindVertexArray(self.gcode_vao)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.gcode_vbo)

        vProjection = gl.glGetUniformLocation(self.simple_object_shader, 'vProjection')
        vPosisition = gl.glGetAttribLocation(self.simple_object_shader, "vPosisition")
        vColor = gl.glGetAttribLocation(self.simple_object_shader, "vColor")
        vCamera = gl.glGetUniformLocation(self.simple_object_shader, 'vCamera')

        gl.glUniformMatrix4fv(vProjection, 1, gl.GL_FALSE, self.projection_matrix_function())
        gl.glUniformMatrix4fv(vCamera, 1, gl.GL_FALSE, self.camera_matrix_function())

        gl.glEnableVertexAttribArray(vPosisition)
        gl.glEnableVertexAttribArray(vColor)

        gl.glVertexAttribPointer(vPosisition, 4, gl.GL_FLOAT, gl.GL_FALSE, 0, None)
        gl.glVertexAttribPointer(vColor, 4, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(self.gcode_size * 4))

        gl.glDrawArrays(gl.GL_LINES, 0, self.gcode_size / 4)
