from scene import Scene
import colors
from ball import Ball
from volume import Volume

from pprint import pprint

import random
import sys
random.seed()

NUM_OBJECTS = 25 # Number of objects in the scene

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
        
        # currently collecting start and end of AABB as position (x,y,z) +- radius/2 instead of axial projections
        # store start and end of object boundaries along each axis, used to determine if collision is occurring

        # sort all 3 lists based on the beginning positions of the AABBs since some objects' positions may have changed
        self.xList.sort(key = lambda el: el[1])
        self.yList.sort(key = lambda el: el[1])
        self.zList.sort(key = lambda el: el[1])

        #for i in range(NUM_OBJECTS):
        #    print self.objects_3d[i]
        #    print self.xList

        # Now check for collisions
        
        xPotentialCollisions = [] # Potential collisions along x axis
        yPotentialCollisions = [] # Potential collisions along y axis
        zPotentialCollisions = [] # Potential collisions along z axis
        PotentialCollisions = [] # Combined list of potential collisions
        finalPotentialCollisions = [] # Final list of potential collisions, after removing duplicates

        for i in range(NUM_OBJECTS):
            j = i-1
            while j >= 0 and self.xList[i][1] < self.xList[j][2]: # start of obj i < end of obj j implies they are colliding along X axis
                xPotentialCollisions.append([self.xList[i][0], self.xList[j][0]]) # append indices of potentially colliding objects
                j -= 1
            j = i+1
            while j < len(self.xList) and self.xList[i][2] > self.xList[j][1]: # end of obj i > start of obj j implies they are colliding along X axis
                xPotentialCollisions.append([self.xList[i][0], self.xList[j][0]]) # append indices of potentially colliding objects
                j += 1

        for i in range(NUM_OBJECTS):
            j = i-1
            while j >= 0 and self.yList[i][1] < self.yList[j][2]: # start of obj i < end of obj j implies they are colliding along Y axis
                yPotentialCollisions.append([self.yList[i][0], self.yList[j][0]]) # append indices of potentially colliding objects
                j -= 1
            j = i+1
            while j < len(self.yList) and self.yList[i][2] > self.yList[j][1]: # end of obj i > start of obj j implies they are colliding along Y axis
                yPotentialCollisions.append([self.yList[i][0], self.yList[j][0]]) # append indices of potentially colliding objects
                j += 1

        for i in range(NUM_OBJECTS):
            j = i-1
            while j >= 0 and self.zList[i][1] < self.zList[j][2]: # start of obj i < end of obj j implies they are colliding along Z axis
                zPotentialCollisions.append([self.zList[i][0], self.zList[j][0]]) # append indices of potentially colliding objects
                j -= 1
            j = i+1
            while j < len(self.zList) and self.zList[i][2] > self.zList[j][1]: # end of obj i > start of obj j implies they are colliding along Z axis
                zPotentialCollisions.append([self.zList[i][0], self.zList[j][0]]) # append indices of potentially colliding objects
                j += 1

        for [a, b] in xPotentialCollisions:
            if ([a, b] in yPotentialCollisions or [b, a] in yPotentialCollisions) and ([a, b] in zPotentialCollisions or [b, a] in zPotentialCollisions):
                PotentialCollisions.append([a, b])
        #print PotentialCollisions, 'PotentialCollisions'
        
        for val in PotentialCollisions:
            if val not in finalPotentialCollisions and val.reverse() not in finalPotentialCollisions:
                finalPotentialCollisions.append(val)

        #print xPotentialCollisions, 'xPotentialCollisions'
        #print yPotentialCollisions, 'yPotentialCollisions'
        #print zPotentialCollisions, 'zPotentialCollisions'
        #print finalPotentialCollisions, 'finalPotentialCollisions'

        # Adjust velocities of colliding objects
        for i in range(len(finalPotentialCollisions)):
            idx1 = finalPotentialCollisions[i][0]
            idx2 = finalPotentialCollisions[i][1]
            self.objects_3d[idx1].reflect()
            self.objects_3d[idx2].reflect()
            
        # call the super class update method
        super(SAPScene, self).update(delta)

    def draw(self):
        # call the super class draw method
        super(SAPScene, self).draw()