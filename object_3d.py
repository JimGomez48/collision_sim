__author__ = 'james'

from pyglet.gl import *


class Object3D(object):
    """
    Basic 3D object class. All other 3D object concrete classes should inherit from
    this class.
    """

    RM = (GLfloat * 16)()   # Temporary Rotation matrix
    TM = (GLfloat * 16)()   # Temporary Translation matrix
    OM = (GLfloat * 16)()   # Orientation i.e Combined Rotation and Translation

    def __init__(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glGetFloatv(GL_MODELVIEW_MATRIX, self.RM)
        glGetFloatv(GL_MODELVIEW_MATRIX, self.TM)
        glGetFloatv(GL_MODELVIEW_MATRIX, self.OM)
        glPopMatrix()

    def update(self, delta):
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

    def __print_matrix__(self, name, m):
        """
        Prints matrix 'm' with name 'name'

        :param name: A string. The name of the matrix to print
        :param m: A 4x4 GL matrix represented as a 1D array
        """
        print str(name) + ":"
        print "[" + str(m[0]) + ", " + str(m[1]) + ", " +str(m[2]) + ", " + str(m[3])
        print " " + str(m[4]) + ", " + str(m[5]) + ", " +str(m[6]) + ", " + str(m[7])
        print " " + str(m[8]) + ", " + str(m[9]) + ", " +str(m[10]) + ", " + str(m[11])
        print " " + str(m[12]) + ", " + str(m[13]) + ", " +str(m[14]) + ", " + str(m[15]) + "]"