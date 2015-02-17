import unittest
import os
import sys
from mock import patch, call
import OpenGL.GL as gl

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from infrastructure.display_list_builder import DisplayListBuilder
from domain.point import Point


@patch('infrastructure.display_list_builder.gl')
class DisplayListBuilderTest(unittest.TestCase):

    def test_get_list_id_should_create_a_new_display_list(self, mock_gl):
        expected_list_id = gl.GLuint(1)

        mock_gl.glGenLists.return_value = expected_list_id
        mock_gl.GL_COMPILE = gl.GL_COMPILE

        dlb = DisplayListBuilder()
        list_id = dlb.get_list_id([])

        self.assertEquals(expected_list_id, list_id)
        mock_gl.glNewList.assert_called_with(expected_list_id, gl.GL_COMPILE)
        mock_gl.glEndList.assert_called_with()

    def test_get_list_should_create_gl_lines(self, mock_gl):
        mock_gl.GL_LINES = gl.GL_LINES
        x, y, z = 0.5, 0.6, 0.7
        points = [Point(x, y, z, False)]
        dlb = DisplayListBuilder()

        dlb.get_list_id(points)

        mock_gl.glBegin.assert_called_with(gl.GL_LINES)
        mock_gl.glVertex3f.assert_has_calls([call(0.0, 0.0, 0.0), call(x, z, y)])
        mock_gl.glEnd.assert_called_with()

    def test_clear_list_clears_gl_list(self, mock_gl):
        expected_list_id = gl.GLuint(1)

        mock_gl.glGenLists.return_value = expected_list_id
        mock_gl.GL_COMPILE = gl.GL_COMPILE

        dlb = DisplayListBuilder()
        list_id = dlb.get_list_id([])
        dlb.clear_list(list_id)

        mock_gl.glDeleteLists.assert_called_with(list_id, 1)


if __name__ == '__main__':
    unittest.main()
