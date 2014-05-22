__author__ = 'james'

from pyglet.gl import *
from OpenGL.GLUT import *

from Colors import *
from Ball import Ball


class Scene:
    """
    This class holds the scene of the simulation. It is responsible for holding and
    maintaining the objects within the scene.
    """
    ball = None

    def __init__(self):
        self.ball = Ball(RED)
        # glMatrixMode(GL_MODELVIEW)
        # glPushMatrix()
        # glLoadIdentity()
        # self.OM = glGetDoublev(GL_MODELVIEW_MATRIX)
        # glPopMatrix()

    def update(self):
        # rotate objects around z-axis
        # glMatrixMode(GL_MODELVIEW)
        #
        # glPushMatrix()
        # glLoadMatrixd(self.OM)
        # glRotatef(self.angle, 0, 0, 1)
        # self.RM = glGetDoublev(GL_MODELVIEW_MATRIX)
        # glPopMatrix()
        self.ball.update()

    def draw(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        gluLookAt(
            1000, 1000, 2000,   # eye
            0, 0, 0,            # look-at
            0, 1, 0             # up
        )
        self.ball.draw()
        # glLoadMatrixd(self.TM)
        # glMultMatrixd(self.RM)
        # draw enclosing square
        glColor4fv(WHITE)
        glutWireCube(1000)
        # draw solid sphere
        # glColor4fv(RED)
        # glutSolidSphere(50, 30, 20)
        glPopMatrix()

    def __draw_axes__(self, length):
        glMatrixMode(GL_MODELVIEW)

        glPushMatrix()

        glLineWidth(1)
        glBegin(GL_LINES)
        glColor4fv(RED)
        glVertex3f(0, 0, 0)
        glVertex3f(length, 0, 0)

        glColor4fv(GREEN)
        glVertex3f(0, 0, 0)
        glVertex3f(0, length, 0)

        glColor4fv(BLUE)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, length)
        glEnd()
        glLineWidth(1)

        glPopMatrix()