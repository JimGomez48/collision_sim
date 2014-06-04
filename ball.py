from pyglet.gl import *
from OpenGL.GLUT import *

from object_3d import *
import colors

class Ball(Object3D):

    radius = 30
    slices = 30
    stacks = 20

    def __init__(self, color, initxp, inityp, initzp, initxv, inityv, initzv):
        Object3D.__init__(self)
        self.color = color
        
        self.xp = initxp
        self.yp = inityp
        self.zp = initzp
        
        self.xv = initxv
        self.yv = inityv
        self.zv = initzv

    def update(self, delta):
        self.xp += self.xv * delta * 50
        self.yp += self.yv * delta * 50
        self.zp += self.zv * delta * 50
        # glMatrixMode(GL_MODELVIEW)
        # glPushMatrix()
        # glLoadMatrixf(self.OM)
        # glRotatef(delta * 10, 0, 1, 0)  # Rotate about y-axis
        # glGetFloatv(GL_MODELVIEW_MATRIX, self.OM)
        # glPopMatrix()
        pass

    def draw(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glMultMatrixf(self.OM)
        glColor4fv(self.color)
        glMaterialfv(GL_FRONT, GL_SPECULAR, colors.WHITE)
        glMateriali(GL_FRONT, GL_SHININESS, 60)
        glTranslatef(self.xp, self.yp, self.zp)
        
        glutSolidSphere(self.radius, self.slices, self.stacks)
        glPopMatrix()
    
    def reflect(self):
        self.xv *= -1
        self.yv *= -1
        self.zv *= -1
        
        self.xp += 1*self.xv
        self.yp += 1*self.yv
        self.zp += 1*self.zv
    
    def xneg(self):
        return self.xp - self.radius
        
    def xpos(self):
        return self.xp + self.radius
    
    def yneg(self):
        return self.yp - self.radius
        
    def ypos(self):
        return self.yp + self.radius
    
    def zneg(self):
        return self.zp - self.radius
        
    def zpos(self):
        return self.zp + self.radius
    

class CollidableBall(CollidableObject):
    slices = 25
    stacks = 25

    def __init__(self, color, radius=50, mass=10, start_p=Point3(), start_v=Vector3()):
        super(CollidableBall, self).__init__(mass=mass, position=start_p, velocity=start_v)
        self.color = color
        self.radius = radius

    def update(self, delta):
        self.translate_v(self.velocity * delta)
        # check for collisions
        # resolve via elastic bounce
        super(CollidableBall, self).update(delta)

    def draw(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glMultMatrixf(self.OM)
        glColor4fv(self.color)
        glMaterialfv(GL_FRONT, GL_SPECULAR, colors.WHITE)
        glMateriali(GL_FRONT, GL_SHININESS, 60)
        # glutSolidCube(self.radius)
        # glutSolidCone(self.radius, self.radius * 1.5, 20, 20)
        glutSolidSphere(self.radius, self.slices, self.stacks)
        # self.__draw_axes__(self.radius * 2)
        glPopMatrix()

    def is_colliding(self, ball):
        # assert isinstance(ball.position, CollidableObject)
        dist = distance(self.position(), ball.position())
        if self.radius + ball.radius >= dist:
            return True
            print "Collision"
        return False
