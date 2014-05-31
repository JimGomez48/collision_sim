from scene import Scene
import colors
from cube import Cube
from ball import Ball
from volume import Volume

from pprint import pprint

import random
random.seed()

NUM_OBJECTS = 15 # Number of objects in the scene

class BruteForceScene(Scene):

    PosList = xList = yList = zList = []
    def __init__(self):
        super(BruteForceScene, self).__init__()
        a1 = random.randint(-500,500)
        a2 = random.randint(-500,500)
        a3 = random.randint(-500,500)
        a4 = random.randint(-1,1) - a1/100
        a5 = random.randint(-1,1) - a2/100
        a6 = random.randint(-1,1) - a3/100
        self.add_object_3d(Ball(colors.RED, a1, a2, a3, a4, a5, a6))
        
        for i in range(NUM_OBJECTS-1):
            initxp = random.randint(-500,500)
            inityp = random.randint(-500,500)
            initzp = random.randint(-500,500)
            initxdv = random.randint(-1,1) - initxp/100
            initydv = random.randint(-1,1) - inityp/100
            initzdv = random.randint(-1,1) - initzp/100
            self.add_object_3d(Ball(colors.BLUE, initxp, inityp, initzp, initxdv, initydv, initzdv))

        #self.add_object_3d(Volume(colors.WHITE))

    def printinfo(self, i):
        return "(" + str(self.objects_3d[i].xp) + " " + str(self.objects_3d[i].yp) + " " + str(self.objects_3d[i].zp) + ") (" + str(self.objects_3d[i].xv) + " " + str(self.objects_3d[i].yv) + " " + str(self.objects_3d[i].zv) + ")"

    def update(self, delta):
        print "0 " + self.printinfo(0)
        # check for collisions
        for i in range(NUM_OBJECTS):
            for j in range(i+1, NUM_OBJECTS):
                if self.collides(i,j):
                    if i==0:
                        print str(j) + " " + self.printinfo(j)
                    self.objects_3d[i].reflect()
                    self.objects_3d[j].reflect()
        
        # call the super class update method
        super(BruteForceScene, self).update(delta)
    
    def collides(self, i,j):
        o1 = self.objects_3d[i]
        o2 = self.objects_3d[j]
        if (o1.xneg() > o2.xneg() and o1.xneg() < o2.xpos()) or (o1.xpos() > o2.xneg() and o1.xpos() < o2.xpos()):
            if (o1.yneg() > o2.yneg() and o1.yneg() < o2.ypos()) or (o1.ypos() > o2.yneg() and o1.ypos() < o2.ypos()):
                if (o1.zneg() > o2.zneg() and o1.zneg() < o2.zpos()) or (o1.zpos() > o2.zneg() and o1.zpos() < o2.zpos()):
                    return 1
        return 0
    
    def draw(self):
        # call the super class draw method
        super(BruteForceScene, self).draw()
