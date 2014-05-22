__author__ = 'james'

from pyglet.gl import *
# from OpenGL.GL import *


class Object3D:
    """
    Basic 3D object class. All other 3D object concrete classes should inherit from
    this class.
    """

    RM = []     # Temporary Rotation matrix
    TM = []     # Temporary Translation matrix
    OM = []     # Orientation i.e Combined Rotation and Translation

    def __init__(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        self.RM = glGetDoublev(GL_MODELVIEW_MATRIX)
        self.TM = glGetDoublev(GL_MODELVIEW_MATRIX)
        self.OM = glGetDoublev(GL_MODELVIEW_MATRIX)
        glPopMatrix()

    def update(self):
        """
        Updates the state of this 3D object
        """
        pass

    def draw(self):
        """
        Draws the current state of this 3D object
        """
        pass

    def rotate(self, angle, axis):
        """
        Rotates this 3D object about the specified axis by the specified angle

        :param angle: A float value. The amount to rotate by
        :param axis: A 3-element array representing the axis of rotation
        """
        # TODO
        pass

    def translate(self, x, y, z):
        """
        Translates this 3D object by the specified ammounts

        :param x: A float value. The amount to translate along the x-axis
        :param y: A float value. The amount to translate along the y-axis
        :param z: A float value. The amount to translate along the z-axis
        """
        # TODO
        pass