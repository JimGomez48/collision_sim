"""
A 3D vector/point module
"""
__author__ = 'james'

import math


class Vector3(object):
    """
    A 3D vector or point.
    """
    def __init__(self, x=0., y=0., z=0.):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __len__(self):
        return 3

    def __add__(self, val):
        """A + B both vectors"""
        return Point3(self[0] + val[0], self[1] + val[1], self[2] + val[2])

    def __sub__(self, val):
        """A - B both vectors"""
        return Point3(self[0] - val[0], self[1] - val[1], self[2] - val[2])

    def __iadd__(self, val):
        """A += B both vectors"""
        self.x = val[0] + self.x
        self.y = val[1] + self.y
        self.z = val[2] + self.z
        return self

    def __isub__(self, val):
        """A -= B both vectors"""
        self.x = self.x - val[0]
        self.y = self.y - val[1]
        self.z = self.z - val[2]
        return self

    def __div__(self, val):
        """A / b, where b is a scalar"""
        if val == 0:
            return Point3(x=float("inf"), y=float("inf"), z=float("inf"))
        return Point3(x=self[0] / val, y=self[1] / val, z=self[2] / val)

    def __mul__(self, val):
        """a * B, where a is a scalar"""
        return Point3(self[0] * val, self[1] * val, self[2] * val)

    def __idiv__(self, val):
        """A /= b, where b is a scalar"""
        if val == 0:
            self = Point3(x=float("inf"), y=float("inf"), z=float("inf"))
        else:
            self[0] = self[0] / val
            self[1] = self[1] / val
            self[2] = self[2] / val
        return self

    def __imul__(self, val):
        """A *= b, where b is a scalar"""
        self[0] = self[0] * val
        self[1] = self[1] * val
        self[2] = self[2] * val
        return self

    def __getitem__(self, key):
        """get index with []"""
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        elif key == 2:
            return self.z
        else:
            raise Exception("Can only index 0, 1, or 2")

    def __setitem__(self, key, value):
        """ set index with []"""
        if key == 0:
            self.x = float(value)
        elif key == 1:
            self.y = float(value)
        elif key == 2:
            self.z = float(value)
        else:
            raise Exception("Can only index 0, 1, or 2")

    def __eq__(self, other):
        """== if components are within 0.0001 of each other"""
        if math.fabs(self.x - other.x) > 0.0001:
            return False
        if math.fabs(self.y - other.y) > 0.0001:
            return False
        if math.fabs(self.z - other.z) > 0.0001:
            return False
        return True

    def __str__(self):
        """to string"""
        return "[" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + "]"

    def is_zero_vector(self):
        return self.x == 0 and self.y == 0 and self.z == 0
Point3 = Vector3


def distance_squared(point1, point2):
    """
    Returns the distance between two points squared. Marginally faster than
    Distance()
    """
    return (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 + \
           (point1[2] - point2[2]) ** 2


def distance(point1, point2):
    """Returns the distance between two points"""
    return math.sqrt(distance_squared(point1, point2))


def mag_squared(vec):
    """
    Returns the magnitude of a vector squared. Faster than mag(),
    but only marginally
    """
    return vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2


def mag(vec):
    """Returns the magnitude of a vector"""
    return math.sqrt(mag_squared(vec))


def normalize(vec):
    """
    Returns a new vector that has the same direction as vec, but has a
    length of one.
    """
    if vec[0] == 0. and vec[1] == 0. and vec[2] == 0.:
        return Vector3(0., 0., 0.)
    return vec / mag(vec)


def dot(a, b):
    """Computes the dot product of a and b"""
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a, b):
    """Computes the cross product vector of a and b"""
    return Point3(
        a[1] * b[2] - b[1] * a[2],
        b[0] * a[2] - a[0] * b[2],
        a[0] * b[1] - b[0] * a[1]
    )


def project_onto(w, v):
    """Projects w onto v."""
    return v * dot(w, v) / mag_squared(v)
