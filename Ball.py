__author__ = 'james'

from pyglet.gl import *
from OpenGL.GLUT import *

from Object3D import Object3D


class Ball(Object3D):

    def __init__(self, color):
        Object3D.__init__(self)
        self.color = color

    def update(self, delta):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        # TODO: ROTATE THE BALL
        glPopMatrix()
        pass

    def draw(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        # glLoadMatrixf(self.OM)
        glColor4fv(self.color)
        glutSolidSphere(50, 30, 20)
        glutSolidSphere(50, 30, 20)
        glPopMatrix()

