import OpenGL.GL as gl
import OpenGL.GLUT as glut


class DisplayListBuilder(object):
    def get_list_id(self, points):
        display_list_id = gl.glGenLists(1)
        gl.glNewList(display_list_id, gl.GL_COMPILE)
        gl.glEndList()
        return display_list_id

    def clearList(self, id):
        pass
