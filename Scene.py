__author__ = 'james'

from pyglet.gl import *
from OpenGL.GLUT import *

import Colors
from Ball import Ball


class Scene:
    """
    This class holds the scene of the simulation. It is responsible for holding and
    maintaining the objects within the scene.
    """
    objects_3d = []

    def __init__(self):
        self.objects_3d.append(Ball(Colors.RED))

    def update(self, delta):
        # print "Delta Time: " + str(delta) + " secs"
        for o in self.objects_3d:
            o.update(delta)

    def draw(self):
        self.__set_lighting()

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        gluLookAt(
            1000, 800, 2000,    # eye
            0, 0, 0,            # look-at
            0, 1, 0             # up
        )
        # draw white cube
        glColor4fv(Colors.WHITE)
        glutWireCube(1000)
        # draw objects in the object list
        for o in self.objects_3d:
            o.draw()
        self.__draw_axes(1200)
        glPopMatrix()

    def __set_lighting(self):
        # glClearColor(0.5, 0.7, 0.9, 1.0)  # sky bg
        glClearColor(0.0, 0.0, 0.0, 1.0)  # black bg
        # glClearColor(1.0, 1.0, 1.0, 1.0)  # white bg
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glShadeModel(GL_SMOOTH)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)

        # set light 0 as diffuse directional light
        diffuse_pos = (gl.GLfloat * 4)(*[1000.0, 1000.0, 500.0, 0.0])
        glLightfv(GL_LIGHT0, GL_POSITION, diffuse_pos)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, Colors.OFF_WHITE)
        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
        glEnable(GL_LIGHT0)

        # add ambient lighting
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, Colors.DARK_GRAY)

    def __draw_axes(self, length):
        glMatrixMode(GL_MODELVIEW)

        glPushMatrix()

        glLineWidth(1)
        glBegin(GL_LINES)
        glColor4fv(Colors.RED)
        glVertex3f(0, 0, 0)
        glVertex3f(length, 0, 0)

        glColor4fv(Colors.GREEN)
        glVertex3f(0, 0, 0)
        glVertex3f(0, length, 0)

        glColor4fv(Colors.BLUE)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, length)
        glEnd()
        glLineWidth(1)

        glPopMatrix()