__author__ = 'james'

from pyglet.gl import *
from OpenGL.GLUT import *

from Object3D import Object3D
import Colors


class Volume(Object3D):

    def __init__(self, color):
        Object3D.__init__(self)
        self.color = color

    def update(self, delta):
        # currently just rotating about y-axis on every frame
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadMatrixf(self.OM)
        glRotatef(delta * 10, 0, 1, 0)  # Rotate about y-axis
        glGetFloatv(GL_MODELVIEW_MATRIX, self.OM)
        glPopMatrix()
        pass

    def draw(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glMultMatrixf(self.OM)
        glScalef(1.5, 1.0, 1.0)
        glColor4fv(self.color)
        glMaterialfv(GL_FRONT, GL_SPECULAR, Colors.WHITE)
        glMateriali(GL_FRONT, GL_SHININESS, 60)
        glutWireCube(1000)
        glPopMatrix()
