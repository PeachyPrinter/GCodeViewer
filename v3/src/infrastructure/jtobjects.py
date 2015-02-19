import OpenGL.GL as gl
import numpy as np
import os
import ctypes

from shader_loader import ShaderLoader


class JTObjects(object):
    def __init__(self, resource_path, projection_matrix_function, camera_matrix_function):
        self.resource_path = resource_path
        self.projection_matrix_function = projection_matrix_function
        self.camera_matrix_function = camera_matrix_function
        self.load_shader_programs()
        self.init_grid()

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

                                    -1.0,    -1.0,     0.0,    1.0,
                                     1.0,    -1.0,     0.0,    1.0,
                                     1.0,     1.0,     0.0,    1.0,
                                     1.0,     1.0,     0.0,    1.0,
                                    -1.0,     1.0,     0.0,    1.0,
                                    -1.0,    -1.0,     0.0,    1.0,

                                     0.0,    -1.0,    -1.0,    1.0,
                                     0.0,     1.0,    -1.0,    1.0,
                                     0.0,     1.0,     1.0,    1.0,
                                     0.0,     1.0,     1.0,    1.0,
                                     0.0,    -1.0,     1.0,    1.0,
                                     0.0,    -1.0,    -1.0,    1.0,
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

