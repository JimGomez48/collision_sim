__author__ = 'james'

from pyglet.gl import *

import colors
from ball import Ball
from volume import Volume


class Scene(object):
    """
    This class holds the scene of the simulation. It is responsible for holding and
    maintaining the objects within the scene.
    """
    objects_3d = []
    fps_display = pyglet.clock.ClockDisplay()
    num_objects = 50

    def __init__(self, num_objects):
        self.num_objects = num_objects

    def update(self, delta):
        """
        Updates the scene, including all 3D objects

        :param delta: A float value. The amount of time in seconds that has elapsed
        since the last call to this method
        """
        for o in self.objects_3d:
            o.update(delta)

        # display FPS
        self.fps_display.draw()

    def draw(self):
        """
        Draw the scene, including all 3D objects
        """
        self.__set_lighting__()

        # set camera position
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        gluLookAt(
            500, 300, 2000,     # eye
            0, 0, 0,            # look-at
            0, 1, 0             # up
        )

        # draw objects in the object list
        for o in self.objects_3d:
            o.draw()
        # self.__draw_axes__(1500)
        glPopMatrix()

    def add_object_3d(self, obj):
        self.objects_3d.append(obj)
    
    def remove_last_object_3d(self):
        self.objects_3d.pop()
    
    def __set_lighting__(self):
        """
        Provides lighting for the scene. Includes Ambient light and a
        Diffuse/Specular directional light
        """
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
        glLightfv(GL_LIGHT0, GL_DIFFUSE, colors.OFF_WHITE)
        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
        glLightfv(GL_LIGHT0, GL_SPECULAR, colors.WHITE)
        glEnable(GL_LIGHT0)

        # add ambient lighting
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, colors.DARK_GRAY)

    def __draw_axes__(self, length):
        """
        Draws a set of world axes centered at the origin

        :param length: The length to draw each of the axes
        """
        glDisable(GL_LIGHTING)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLineWidth(1)
        glBegin(GL_LINES)
        glColor4fv(colors.RED)
        glVertex3f(0, 0, 0)
        glVertex3f(length, 0, 0)
        glColor4fv(colors.GREEN)
        glVertex3f(0, 0, 0)
        glVertex3f(0, length, 0)
        glColor4fv(colors.BLUE)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, length)
        glEnd()
        glLineWidth(1)
        glPopMatrix()
        glEnable(GL_LIGHTING)
