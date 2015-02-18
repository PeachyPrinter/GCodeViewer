import OpenGL.GL as gl
import numpy as np
import ctypes
import os
import logging

from shader_loader import ShaderLoader
from PIL import Image


class JTGLText(object):
    def __init__(self, resource_location, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height

        logging.info("X / Y : %s / %s" % (window_width, window_height))
        self.text_width = 6.0
        self.text_height = self.text_width * 2.0
        self.kern = 1.0

        self.text_size = 0
        self.color_size = 0
        self.last_text = ''
        self.last_color = [0.0, 0.0, 0.0, 1.0]
        self.dirty = True


        text_vertex_shader = os.path.join(resource_location, 'shaders', 'text_shader_vr.glsl')
        text_fragme_shader = os.path.join(resource_location, 'shaders', 'text_shader_fr.glsl')
        self._text_shader_program = ShaderLoader.load_shaders(text_vertex_shader, text_fragme_shader)

        font_texture_path = os.path.join(resource_location, 'textures', 'courier10.png')
        self.font_texture_id = self._load_font_texture(font_texture_path)

        self.text_vao = gl.glGenVertexArrays(1)
        self.text_vbo = gl.glGenBuffers(1)

    def viewPortChanged(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        logging.info("X / Y : %s / %s" % (self.window_width, self.window_height))
        self.dirty = True

    def _load_font_texture(self, location):
        im = Image.open(location)
        image = im.tostring("raw", "RGBA", 0, -1)
        texture_id = gl.glGenTextures(1)
        gl.glActiveTexture(gl.GL_TEXTURE1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, texture_id)
        gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA,  im.size[0], im.size[1], 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, image)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        return texture_id

    def square(self, tl, br):
        a = tl
        b = [br[0], tl[1]]
        c = [tl[0], br[1]]
        d = br
        return [a, b, c, c, b, d]

    def _load_text(self, text, color):
        posisitions = []
        colors = []
        texture_coords = []
        texture_spacing = 1.0 / 510.0
        y_pos = self.window_height - (self.kern + self.text_height)
        x_pos = self.kern
        for char in text:
            if "\n" == char:
                y_pos -= self.text_height + self.kern
                x_pos = self.kern
            else:
                x1 = x_pos
                y1 = y_pos + self.text_height
                x2 = x1 + self.text_width
                y2 = y_pos
                posisitions += self.square([x1, y1], [x2, y2])
                letter_start = (ord(char) * 2.0 * texture_spacing)
                colors += [color for i in range(0, 6)]
                texture_coords += self.square([letter_start, 1], [letter_start + texture_spacing, 0])
                x_pos += self.text_width + self.kern

        posisitions = np.array(posisitions, dtype=np.float32).flatten()
        colors = np.array(colors, dtype=np.float32).flatten()
        texture_coords = np.array(texture_coords, dtype=np.float32).flatten()

        gl.glBindVertexArray(self.text_vao)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.text_vbo)

        gl.glBufferData(gl.GL_ARRAY_BUFFER, (posisitions.size + colors.size + texture_coords.size) * 4, None, gl.GL_STATIC_DRAW)
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, 0, posisitions)
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, posisitions.size * 4, colors)
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, (posisitions.size + colors.size) * 4, texture_coords)

        self.text_size = posisitions.size
        self.color_size = colors.size

    def printgl(self, text, color=[1.0, 1.0, 1.0, 1.0]):
        if self.last_text != text or self.last_color != color or self.dirty:
            self._load_text(text, color)
            self.last_text = text
            self.last_color = color
            self.dirty = False

        gl.glUseProgram(self._text_shader_program)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        gl.glBindVertexArray(self.text_vao)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.text_vbo)

        vPosisition = gl.glGetAttribLocation(self._text_shader_program, "vPosisition")
        vColor = gl.glGetAttribLocation(self._text_shader_program, "vColor")
        vTexCoord = gl.glGetAttribLocation(self._text_shader_program, "vTexCoord")
        vWindow = gl.glGetUniformLocation(self._text_shader_program, 'vWindow')

        gl.glUniform2fv(vWindow, 1, [self.window_width, self.window_height])

        gl.glEnableVertexAttribArray(vPosisition)
        gl.glEnableVertexAttribArray(vColor)
        gl.glEnableVertexAttribArray(vTexCoord)

        texture_data = gl.glGetUniformLocation(self._text_shader_program, "texture_data")
        gl.glUniform1i(texture_data, 1)
        gl.glActiveTexture(gl.GL_TEXTURE1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.font_texture_id)

        gl.glVertexAttribPointer(vPosisition, 2, gl.GL_FLOAT, gl.GL_FALSE, 0, None)
        gl.glVertexAttribPointer(vColor, 4, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(self.text_size * 4))
        gl.glVertexAttribPointer(vTexCoord, 2, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p((self.text_size+self.color_size) * 4))

        gl.glDrawArrays(gl.GL_TRIANGLES, 0, self.text_size / 2)
        gl.glDisable(gl.GL_BLEND)
