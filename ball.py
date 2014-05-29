from pyglet.gl import *
from OpenGL.GLUT import *

from object_3d import Object3D
import colors

class Ball(Object3D):

    def __init__(self, color, initxp, inityp, initzp, initxdv, initydv, initzdv):
        Object3D.__init__(self)
        self.color = color
        
        self.initxp = initxp
        self.inityp = inityp
        self.initzp = initzp
        
        self.initxv = self.inityv = self.initzv = 0
        self.initxdv = initxdv
        self.initydv = initydv
        self.initzdv = initzdv

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
        glTranslatef(self.initxp, self.inityp, self.initzp)
        self.initxv += self.initxdv
        self.inityv += self.initydv
        self.initzv += self.initzdv
        glTranslatef(self.initxv, self.inityv, self.initzv)
        glutSolidSphere(80, 30, 20)
        glPopMatrix()
