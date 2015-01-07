from OpenGL.GL import *
from OpenGL.GLUT import *

class PGAbstract(object):
    def draw(self):
        self.process()

class PGLine(PGAbstract):
    def __init__(self, start, end, colour):
        return PGLinesWrapper(self,start,[end],colour)

class PGLines(PGAbstract):
    def __init__(self, start, segments, colour):
        self.start = start
        self.segs = segments
        self.colour = colour

    def process(PGAbstract):
        glBegin(GL_LINES)
        glColor3fv(self.colour)
        last = self.start
        for segment in self.segs:
            glVertex3f(last)
            glVertex3f(segment)
            last = segment
        glEnd()

class PGObject(PGAbstract):
    def __init__(self):
        self._items = []

    def append(item):
        self._items.append(item)

    def process(self):
        for item in self._items:
            item.draw()



