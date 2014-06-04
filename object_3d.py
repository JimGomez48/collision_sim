__author__ = 'james'

from pyglet.gl import *
import math

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
        # self.print_matrix("TM", self.TM)
        self.__reset_matrix__(self.RM)
        self.__reset_matrix__(self.TM)
        glGetFloatv(GL_MODELVIEW_MATRIX, self.OM)
        glPopMatrix()
        # self.print_matrix("TM", self.TM)

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

    def position(self):
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

    def turn_to_face_v(self, direction=Vector3()):
        """
        Turn this object so that its forward vector coincides with direction

        :param direction: A Vector3. The direction to turn to
        """
        if direction.is_zero_vector():
            return
        direction = normalize(direction)
        forward = self.get_forward()
        axis = cross(forward, direction)
        angle = math.degrees(math.acos(dot(forward, direction)))
        self.rotate(angle=angle, axis=axis)

    def turn_to_face_p(self, target=Point3()):
        """
        Turn this object so that its forward vector points to target.

        :param target: A Point3, The point to face towards
        """
        my_pos = self.position()
        if my_pos == target:
            return
        direction = normalize(target - my_pos)
        self.turn_to_face_v(direction)

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
        glDisable(GL_LIGHTING)
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
        glEnable(GL_LIGHTING)

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


class CollidableObject(Object3D):
    def __init__(self, mass=10, position=Point3(0, 0, 0), velocity=Vector3(0, 0, 0)):
        super(CollidableObject, self).__init__()
        self.mass = mass
        self.translate_v(position)
        self.velocity = velocity

    def is_colliding(self, obj):
        """
        determines whether this object is colliding with object obj. Override in
        concrete subclass to provide specific implementation.

        :param obj: the object to test collision against
        :return: True if the objects are colliding, false otherwise.
        """
        return False

    def elastic_collide(self, obj):
        """
        Resolves collisions in 3-space via elastic collision and the
        conservation of momentum equations

        :param obj: what this object is colliding with
        """
        # CONSERVATION OF MOMENTUM
        # m1*u1 + m2*u2 = m1*v1 + m2*v2
        #
        # CONSERVATION OF ENERGY
        # (m1*u1^2)/2 + (m2*u2^2)/2 = (m1*v1^2)/2 + (m2*u2^2)/2
        # assert isinstance(obj) is CollidableObject
        p1 = self.position()
        p2 = obj.position()
        v1 = self.get_forward() * self.velocity.z
        v2 = obj.get_forward() * obj.velocity.z
        m1 = self.mass
        m2 = obj.mass

        # angle = math.acos(dot(p1, p2) / (normalize(p1) * normalize(p2)))
        # angle = math.degrees(angle)

        v1_new = Vector3()
        v2_new = Vector3()

        v1_new.x = v2.x * (m1 - m2) + 2 * m2 * v2.x
        v1_new.y = v2.y * (m1 - m2) + 2 * m2 * v2.y
        v1_new.z = v2.z * (m1 - m2) + 2 * m2 * v2.z

        v2_new.x = v1.x * (m2 - m1) + 2 * m1 * v1.x
        v2_new.y = v1.y * (m2 - m1) + 2 * m1 * v1.y
        v2_new.z = v1.z * (m2 - m1) + 2 * m1 * v1.z

        self.velocity = v1
        obj.velocity = v2




