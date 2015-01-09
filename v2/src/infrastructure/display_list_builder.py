import OpenGL.GL as gl

from domain.point import Point


class DisplayListBuilder(object):
    def get_list_id(self, points):
        last_point = Point(0.0, 0.0, 0.0, False)
        display_list_id = gl.glGenLists(1)
        gl.glNewList(display_list_id, gl.GL_COMPILE)
        gl.glBegin(gl.GL_LINES)
        gl.glVertex3f(*last_point.xzy)
        for point in points:
            gl.glVertex3f(*point.xzy)
        gl.glEnd()
        gl.glEndList()
        return display_list_id

    def clearList(self, id):
        pass
