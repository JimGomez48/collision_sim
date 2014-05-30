__author__ = 'james'

from pyglet.gl import *

import colors
from vector3 import *


class Object3D(object):
    """
    Basic 3D object class. All other 3D object concrete classes should inherit
    from this class.
    """
    # OpenGL 4x4 orientation matrix for reference
    #
    # [ Rx Ux Fx Tx ]
    # [ Ry Uy Fy Ty ]
    # [ Rz Uz Fz Tz ]
    # [ Rh Uh Fh Th ]
    #
    # The matrix is stored in memory as a column-wise 1-D array

    __Rx = 0    # right x
    __Ry = 1    # right y
    __Rz = 2    # right z
    __Rh = 3    # right homogeneous
    __Ux = 4    # up x
    __Uy = 5    # up y
    __Uz = 6    # up z
    __Uh = 7    # up homogeneous
    __Fx = 8    # forward x
    __Fy = 9    # forward y
    __Fz = 10   # forward z
    __Fh = 11   # forward homogeneous
    __Tx = 12   # translation x
    __Ty = 13   # translation y
    __Tz = 14   # translation z
    __Th = 15   # translation homogeneous

    def __init__(self):
        self.RM = (GLfloat * 16)()  # Stores rotations to be applied to OM
        self.TM = (GLfloat * 16)()  # Stores translations to be applied to OM
        self.OM = (GLfloat * 16)()  # The current orientation matrix
        # load identity matrices into RM, TM, OM
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glGetFloatv(GL_MODELVIEW_MATRIX, self.RM)
        glGetFloatv(GL_MODELVIEW_MATRIX, self.TM)
        glGetFloatv(GL_MODELVIEW_MATRIX, self.OM)
        glPopMatrix()

    def update(self, delta):
        """
        Updates the state of this 3D object by updating the OM matrix. By
        default, applies rotations stored in RM first, then translations stored
        in TM. Can be overriden in child classes for different behavior
        """
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadMatrixf(self.OM)
        glMultMatrixf(self.RM)
        glMultMatrixf(self.TM)
        glGetFloatv(GL_MODELVIEW_MATRIX, self.OM)
        self.print_matrix("TM", self.TM)
        self.__reset_matrix__(self.RM)
        self.__reset_matrix__(self.TM)
        glGetFloatv(GL_MODELVIEW_MATRIX, self.OM)
        glPopMatrix()
        self.print_matrix("TM", self.TM)

    def draw(self):
        """
        Draws the current state of this 3D object. By default, draws nothing.
        Override to provide draw behavior
        """
        pass

    def get_right(self):
        """
        :return: the right vector of this object as a Vector3
        """
        return Vector3(self.OM[self.__Rx], self.OM[self.__Ry], self.OM[self.__Rz])

    def get_up(self):
        """
        :return: the up vector of this object as a Vector3
        """
        return Vector3(self.OM[self.__Ux], self.OM[self.__Uy], self.OM[self.__Uz])

    def get_forward(self):
        """
        :return: the forward vector of this object as a Vector3
        """
        return Vector3(self.OM[self.__Fx], self.OM[self.__Fy], self.OM[self.__Fz])

    def get_position(self):
        """
        :return: the position of this object as a Point3
        """
        return Point3(self.OM[self.__Tx], self.OM[self.__Ty], self.OM[self.__Tz])

    def set_position(self, position=Point3()):
        """
        :param position: A Point3 specifying the world position to set to
        """
        for i in range(3):
            self.OM[self.__Tx + i] = GLfloat(position[i])
        self.OM[self.__Th] = 1.0

    def rotate(self, angle, axis=Vector3(0, 1, 0)):
        """
        Rotates this 3D object about the specified axis by the specified angle.
        (Default axis is y-axis)

        :param angle: the angle to rotate this object by in degrees
        :param axis: a Vector3. the axis to rotate about
        NOTE: rotation will not be applied to OM until update() is called
        """
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadMatrixf(self.RM)
        glRotatef(GLfloat(angle),
                  GLfloat(axis[0]), GLfloat(axis[1]), GLfloat(axis[2]))
        glGetFloatv(GL_MODELVIEW_MATRIX, self.RM)
        glPopMatrix()

    def translate_v(self, trans=Vector3()):
        """
        Translates this 3D object in world coordinates by the translation vector
        (default is 0 translation)

        :param trans: a translation Vector3
        NOTE: translation will not be applied to OM until update() is called
        """
        self.translate(trans[0], trans[1], trans[2])

    def translate(self, x, y, z):
        """
        Translates this 3D object in world coordinates by the translation vector

        :param x: the amount to translate along the x-axis
        :param y: the amount to translate along the y-axis
        :param z: the amount to translate along the z-axis
        NOTE: translation will not be applied to OM until update() is called
        """
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadMatrixf(self.TM)
        glTranslatef(GLfloat(x), GLfloat(y), GLfloat(z))
        glGetFloatv(GL_MODELVIEW_MATRIX, self.TM)
        glPopMatrix()

    def print_matrix(self, name, matrix):
        """
        Prints the specified matrix
        """
        print str(name) + ":"
        print "[" + str(matrix[self.__Rx]) + ", " + str(matrix[self.__Ux]) + \
              ", " + str(matrix[self.__Fx]) + ", " + str(matrix[self.__Tx])
        print " " + str(matrix[self.__Ry]) + ", " + str(matrix[self.__Uy]) + \
              ", " + str(matrix[self.__Fy]) + ", " + str(matrix[self.__Ty])
        print " " + str(matrix[self.__Rz]) + ", " + str(matrix[self.__Uz]) + \
              ", " + str(matrix[self.__Fz]) + ", " + str(matrix[self.__Tz])
        print " " + str(matrix[self.__Rh]) + ", " + str(matrix[self.__Uh]) + \
              ", " + str(matrix[self.__Fh]) + ", " + str(matrix[self.__Th])\
              + "]"

    def __draw_axes__(self, length):
        length = GLfloat(length)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLineWidth(2)
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

    def __list_to_glfloat_array__(self, matrix_list):
        """
        Converts a normal Python list of to a GLfloat array usable by
        OpenGL.

        :param matrix_list: the 16 element list to be converted
        :return: a 1-D GLfloat array
        """
        matrix = (GLfloat * len(matrix_list))()
        for i in range(len(matrix_list)):
            matrix[i] = GLfloat(matrix_list[i])
        return matrix

    def __reset_matrix__(self, matrix):
        """
        Resets a matrix to the identity matrix
        :param matrix: the matrix to be reset
        """
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glGetFloatv(GL_MODELVIEW_MATRIX, matrix)
        glPopMatrix()
