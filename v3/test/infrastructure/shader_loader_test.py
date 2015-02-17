import unittest
import os
import sys
from mock import patch, mock_open
import OpenGL.GLUT as glut
import OpenGL.GL as gl

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from infrastructure.shader_loader import ShaderLoader


class ShaderLoaderTest(unittest.TestCase):
    def setUp(self):
        glut.glutInit()
        glut.glutInitDisplayMode(glut.GLUT_RGBA | glut.GLUT_DOUBLE | glut.GLUT_DEPTH)
        glut.glutInitWindowSize(20, 20)
        self.window_id = glut.glutCreateWindow(self.__class__.__name__)
        self.test_data_path = os.path.join(os.path.dirname(__file__), 'test_data')

    def tearDown(self):
        glut.glutDestroyWindow(self.window_id)

    def test_load_shaders_reads_and_creates_shaders(self):
        result = ShaderLoader.load_shaders(
            os.path.join(self.test_data_path, 'good_vertex.glsl'),
            os.path.join(self.test_data_path, 'good_fragment.glsl')
        )
        self.assertTrue(result)



if __name__ == '__main__':
    unittest.main()
