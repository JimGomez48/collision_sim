__author__ = 'james'

from pyglet.gl import *
from OpenGL.GLUT import *
import random

from object_3d import Object3D
from vector3 import *
import colors


class Cube(Object3D):

    side = 80

    def __init__(self, color, size=50, start_pos=Vector3()):
        super(Cube, self).__init__()
        self.color = color
        self.size = size
        self.translate_v(start_pos)
        self.rotate_axis = Vector3(
            random.random() * random.choice([1, -1]),
            random.random() * random.choice([1, -1]),
            random.random() * random.choice([1, -1])
        )
        self.rotate_axis = normalize(self.rotate_axis)
        self.velocity = Vector3(
            random.random() * random.randint(-200, 200),
            random.random() * random.randint(-200, 200),
            random.random() * random.randint(-200, 200)
        )
        self.rotate_speed = random.randint(-200, 200)

    def update(self, delta):
        self.translate_v(self.velocity * delta)
        self.rotate(self.rotate_speed * delta, self.rotate_axis)
        super(Cube, self).update(delta)

    def draw(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glMultMatrixf(self.OM)
        glColor4fv(self.color)
        glMaterialfv(GL_FRONT, GL_SPECULAR, colors.WHITE)
        glMateriali(GL_FRONT, GL_SHININESS, 60)
        glutSolidCube(self.size)
        # glutSolidCone(self.size, self.size * 1.5, 20, 20)
        # glutSolidSphere(80, 25, 25)
        self.__draw_axes__(100)
        glPopMatrix()


