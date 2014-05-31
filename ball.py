from pyglet.gl import *
from OpenGL.GLUT import *

from object_3d import Object3D
import colors

class Ball(Object3D):

    radius = 80
    slices = 30
    stacks = 20

    def __init__(self, color, initxp, inityp, initzp, initxv, inityv, initzv):
        Object3D.__init__(self)
        self.color = color
        
        self.initxp = initxp
        self.inityp = inityp
        self.initzp = initzp
        
        self.initxv = initxv
        self.inityv = inityv
        self.initzv = initzv

    def update(self, delta):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadMatrixf(self.OM)
        #glRotatef(delta * 10, 0, 1, 0)  # Rotate about y-axis
        glGetFloatv(GL_MODELVIEW_MATRIX, self.OM)
        glPopMatrix()
        pass

    def draw(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glMultMatrixf(self.OM)
        glColor4fv(self.color)
        glMaterialfv(GL_FRONT, GL_SPECULAR, colors.WHITE)
        glMateriali(GL_FRONT, GL_SHININESS, 60)
        self.initxp += self.initxv
        self.inityp += self.inityv
        self.initzp += self.initzv
        glTranslatef(self.initxp, self.inityp, self.initzp)
        
        glutSolidSphere(self.radius, self.slices, self.stacks)
        glPopMatrix()
