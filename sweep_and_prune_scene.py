from scene import Scene
import colors
from ball import Ball
from volume import Volume

from pprint import pprint

import random
import sys
random.seed()

NUM_OBJECTS = 15 # Number of objects in the scene

class SAPScene(Scene):

    PosList = []
    xList = []
    yList = []
    zList = []
    def __init__(self):
        super(SAPScene, self).__init__()
        for i in range(NUM_OBJECTS):
            initxp = random.randint(-500,500)
            inityp = random.randint(-500,500)
            initzp = random.randint(-500,500)
            initxdv = random.randint(-1,1) - initxp/100
            initydv = random.randint(-1,1) - inityp/100
            initzdv = random.randint(-1,1) - initzp/100
            self.add_object_3d(Ball(colors.BLUE, initxp, inityp, initzp, initxdv, initydv, initzdv))
            #self.add_object_3d(Cube(colors.BLUE))

        # currently collecting start and end of AABB as position (x,y,z) +- radius/2 instead of axial projections
        # store start and end of object boundaries along each axis, used to determine if collision is occurring

        for i in range(NUM_OBJECTS):
            self.xList.append([i, self.objects_3d[i].xneg(), self.objects_3d[i].xpos()])
        
        for i in range(NUM_OBJECTS):
            self.yList.append([i, self.objects_3d[i].yneg(), self.objects_3d[i].ypos()])
        
        for i in range(NUM_OBJECTS):
            self.zList.append([i, self.objects_3d[i].zneg(), self.objects_3d[i].zpos()])

        #self.add_object_3d(Volume(colors.WHITE))
        
    def update(self, delta):
        
        # even though the lists are initialized by the constructor, they must be reinitialized each time since object positions change

        # currently collecting start and end of AABB as position (x,y,z) +- radius/2 instead of axial projections
        # store start and end of object boundaries along each axis, used to determine if collision is occurring

        self.xList = []
        self.yList = []
        self.zList = []

        for i in range(NUM_OBJECTS):
            self.xList.append([i, self.objects_3d[i].xneg(), self.objects_3d[i].xpos()])
        
        for i in range(NUM_OBJECTS):
            self.yList.append([i, self.objects_3d[i].yneg(), self.objects_3d[i].ypos()])
        
        for i in range(NUM_OBJECTS):
            self.zList.append([i, self.objects_3d[i].zneg(), self.objects_3d[i].zpos()])

        # sort all 3 lists based on the beginning positions of the AABBs
        self.xList.sort(key = lambda el: el[1])
        self.yList.sort(key = lambda el: el[1])
        self.zList.sort(key = lambda el: el[1])

        # Now check for collisions
        potentialCollisions = [] # presence of (i, j) indicates that the pair is likely to collide
        for i in range(NUM_OBJECTS):
            j = i+1
            while j < len(self.xList) and self.xList[i][2] > self.xList[j][1]: # end of obj i > start of obj j implies they are colliding along X axis 
                potentialCollisions.append([i, j])
                j += 1
            j = i+1
            while j < len(self.yList):
                if self.yList[i][2] > self.yList[j][1] and [i, j] not in potentialCollisions: # end of obj i > start of obj j implies they are colliding along Y axis
                    potentialCollisions.append([i, j])
                elif [i, j] in potentialCollisions: # they don't collide along the Y axis, remove from potential collisions
                    potentialCollisions.remove([i, j])
                j += 1
            j = i+1
            while j < len(self.zList):
                if self.zList[i][2] > self.zList[j][1] and [i, j] not in potentialCollisions: # end of obj i > start of obj j implies they are colliding along Z axis
                    potentialCollisions.append([i, j])
                elif [i, j] in potentialCollisions: # they don't collide along Z axis, remove from potential collisions
                    potentialCollisions.remove([i, j])
                j += 1
            
        # Adjust velocities of colliding objects
        for i in range(len(potentialCollisions)):
            idx1 = potentialCollisions[i][0]
            idx2 = potentialCollisions[i][1]
            if idx1 < len(self.objects_3d):
                self.objects_3d[idx1].reflect()
            else:
                print 'idx1', idx1
            if idx2 < len(self.objects_3d):
                self.objects_3d[idx2].reflect()
            else:
                print 'idx2', idx2
        # call the super class update method
        super(SAPScene, self).update(delta)

    def draw(self):
        # call the super class draw method
        super(SAPScene, self).draw()