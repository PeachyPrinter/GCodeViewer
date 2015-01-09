import unittest
import os
import sys
from mock import patch, MagicMock
import numpy as np
import OpenGL.GL as gl
import OpenGL.GLUT as glut

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from infrastructure.display_list_builder import DisplayListBuilder
from domain.point import Point

@patch('infrastructure.display_list_builder.gl')
@patch('infrastructure.display_list_builder.glut')
class DisplayListBuilderTest(unittest.TestCase):

    def test_get_list_id_should_create_a_new_display_list(self, mock_glut, mock_gl):
        expected_list_id = gl.GLuint(1)

        mock_gl.glGenLists.return_value = expected_list_id
        mock_gl.GL_COMPILE = gl.GL_COMPILE

        dlb = DisplayListBuilder()
        list_id = dlb.get_list_id([])

        self.assertEquals(expected_list_id, list_id)
        mock_gl.glNewList.assert_called_with(expected_list_id, gl.GL_COMPILE)
        mock_gl.glEndList.assert_called_with()

if __name__ == '__main__':
    unittest.main()
