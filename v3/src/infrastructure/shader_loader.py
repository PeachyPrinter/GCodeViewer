import logging
import OpenGL.GL as gl


class ShaderLoader(object):

    @classmethod
    def load_vertex_shader(cls, file_path):
        shader_id = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        with open(file_path, 'r') as file_handle:
            code = file_handle.read()

        logging.info("Compiling shader : %s" % file_path)
        gl.glShaderSource(shader_id, code)
        gl.glCompileShader(shader_id)

        result = gl.glGetShaderiv(shader_id, gl.GL_COMPILE_STATUS)
        info = gl.glGetShaderInfoLog(shader_id)
        logging.info("Result: %s" % result)
        logging.info("Info: %s" % info)
        if info:
            raise Exception(info)

        return shader_id

    @classmethod
    def load_fragment_shader(cls, file_path):
        shader_id = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        with open(file_path, 'r') as file_handle:
            code = file_handle.read()

        logging.info("Compiling shader : %s" % file_path)
        gl.glShaderSource(shader_id, code)
        gl.glCompileShader(shader_id)

        result = gl.glGetShaderiv(shader_id, gl.GL_COMPILE_STATUS)
        info = gl.glGetShaderInfoLog(shader_id)
        logging.info("Result: %s" % result)
        logging.info("Info: %s" % info)
        if info:
            raise Exception(info)

        return shader_id

    @classmethod
    def load_shaders(cls, vertex_shader_file, fragment_shader_file):
        shader_program = gl.glCreateProgram()

        vertex_shader_id = cls.load_vertex_shader(vertex_shader_file)
        fragment_shader_id = cls.load_fragment_shader(fragment_shader_file)

        logging.info("Creating shader program")
        gl.glAttachShader(shader_program, vertex_shader_id)
        gl.glAttachShader(shader_program, fragment_shader_id)
        gl.glLinkProgram(shader_program)

        result = gl.glGetProgramiv(shader_program, gl.GL_LINK_STATUS)
        info = gl.glGetProgramInfoLog(shader_program)
        logging.info("Result: %s" % result)
        logging.info("Info: %s" % info)
        if info:
            raise Exception(info)

        gl.glDeleteShader(vertex_shader_id)
        gl.glDeleteShader(fragment_shader_id)

        return shader_program
