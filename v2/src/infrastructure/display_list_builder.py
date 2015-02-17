import OpenGL.GL as gl

from domain.point import Point


class DisplayListBuilder(object):
    def get_list_id(self, points):
        last_point = Point(0.0, 0.0, 0.0, False)
        display_list_id = gl.glGenLists(1)
        gl.glNewList(display_list_id, gl.GL_COMPILE)
        gl.glBegin(gl.GL_LINES)
        gl.glVertex3f(*last_point.xzy)
        point_cnt = 0
        for point in points:
            point_cnt += 1
            if point_cnt % 1000 == 0:
                print("Loading: %s" % point_cnt)
            gl.glVertex3f(*point.xzy)
        gl.glEnd()
        gl.glEndList()
        return display_list_id

    def clear_list(self, id):
        gl.glDeleteLists(id, 1)
