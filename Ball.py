__author__ = 'james'

from pyglet.gl import *
from OpenGL.GLUT import *
# from OpenGL.GLU import *
# from OpenGL.GL import *

from Object3D import Object3D
from Colors import *

class Ball(Object3D):
    color = RED

    def __init__(self, color):
        Object3D.__init__(self)
        self.color = color

    def update(self):
        # do a simple rotation 2 degrees each step
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadMatrixd(self.OM)
        glRotated(float(2.0), 0, 0, 1)
        self.OM = glGetDoublev(GL_MODELVIEW_MATRIX)
        glPopMatrix()

    def draw(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadMatrixd(self.OM)
        glColor4fv(self.color)
        glutSolidSphere(50, 30, 20)
        glPopMatrix()

