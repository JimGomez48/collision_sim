__author__ = 'james'

from pyglet.gl import *
from OpenGL.GLUT import *
import random

from object_3d import Object3D
import colors


class Cube(Object3D):

    def __init__(self, color):
        super(Cube, self).__init__()
        self.color = color
        self.axis = [
            random.random() * random.choice([1, -1]),
            random.random() * random.choice([1, -1]),
            random.random() * random.choice([1, -1])
        ]
        self.axis = self.__normalize_vector__(self.axis)
        self.start = [
            random.randint(-500,500),
            random.randint(-500,500),
            random.randint(-500,500)
        ]
        self.velocity = [
            random.random() * random.randint(-200, 200),
            random.random() * random.randint(-200, 200),
            random.random() * random.randint(-200, 200)
        ]
        self.rotate_speed = random.randint(-200, 200)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glTranslatef(
            GLfloat(self.start[0]),
            GLfloat(self.start[0]),
            GLfloat(self.start[0])
        )
        glGetFloatv(GL_MODELVIEW_MATRIX, self.OM)
        glPopMatrix()

    def update(self, delta):
        self.translate(
            self.velocity[0] * delta,
            self.velocity[1] * delta,
            self.velocity[2] * delta
        )
        self.rotate(self.rotate_speed * delta, self.axis)
        super(Cube, self).update(delta)

    def draw(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glMultMatrixf(self.OM)
        glColor4fv(self.color)
        glMaterialfv(GL_FRONT, GL_SPECULAR, colors.WHITE)
        glMateriali(GL_FRONT, GL_SHININESS, 60)
        glutSolidCube(80)
        # glutSolidSphere(80, 25, 25)
        # self.__draw_axes__(200)
        glPopMatrix()


