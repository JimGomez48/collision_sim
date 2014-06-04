__author__ = 'james'

import numpy
from pyglet.gl import *

"""
4fv Color constants for convenience
"""

# gray-scale
WHITE = (gl.GLfloat * 4)(*[1.0, 1.0, 1.0, 1.0])
OFF_WHITE = (gl.GLfloat * 4)(*[0.9, 0.9, 0.9, 1.0])
SILVER = (gl.GLfloat * 4)(*[0.8, 0.8, 0.8, 1.0])
LIGHT_GRAY = (gl.GLfloat * 4)(*[0.7, 0.7, 0.7, 1.0])
GRAY = (gl.GLfloat * 4)(*[0.6, 0.6, 0.6, 1.0])
DARK_GRAY = (gl.GLfloat * 4)(*[0.4, 0.4, 0.4, 1.0])
CHARCOAL = (gl.GLfloat * 4)(*[0.2, 0.2, 0.2, 1.0])
NEAR_BLACK = (gl.GLfloat * 4)(*[0.05, 0.05, 0.05, 1.0])
BLACK = (gl.GLfloat * 4)(*[0.0, 0.0, 0.0, 1.0])

# color
RED = (gl.GLfloat * 4)(*[1.0, 0.0, 0.0, 1.0])
DARK_RED = (gl.GLfloat * 4)(*[0.5, 0.0, 0.0, 1.0])
GREEN = (gl.GLfloat * 4)(*[0.0, 1.0, 0.0, 1.0])
DARK_GREEN = (gl.GLfloat * 4)(*[0.0, 0.2, 0.0, 1.0])
SKY_BLUE = (gl.GLfloat * 4)(*[0.5, 0.7, 0.9, 1.0])
BLUE = (gl.GLfloat * 4)(*[0.0, 0.0, 1.0, 1.0])
DARK_BLUE = (gl.GLfloat * 4)(*[0.0, 0.0, 0.5, 1.0])
YELLOW = (gl.GLfloat * 4)(*[1.0, 1.0, 0.0, 1.0])
PURPLE = (gl.GLfloat * 4)(*[0.4, 0.0, 0.8, 1.0])
ORANGE = (gl.GLfloat * 4)(*[1.0, 0.3, 0.0, 1.0])
MAGENTA = (gl.GLfloat * 4)(*[1.0, 0.0, 1.0, 1.0])
CYAN = (gl.GLfloat * 4)(*[0.0, 1.0, 1.0, 1.0])
