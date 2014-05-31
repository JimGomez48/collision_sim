from scene import Scene
import colors
from cube import Cube
from ball import Ball
from volume import Volume

from pprint import pprint

import random
random.seed()

NUM_OBJECTS = 10 # Number of objects in the scene

class BruteForceScene(Scene):

    PosList = xList = yList = zList = []
    def __init__(self):
        super(BruteForceScene, self).__init__()
        for i in range(NUM_OBJECTS):
            initxp = random.randint(-500,500)
            inityp = random.randint(-500,500)
            initzp = random.randint(-500,500)
            initxdv = random.randint(-1,1) - initxp/100
            initydv = random.randint(-1,1) - inityp/100
            initzdv = random.randint(-1,1) - initzp/100
            self.add_object_3d(Ball(colors.BLUE, initxp, inityp, initzp, initxdv, initydv, initzdv))

        self.add_object_3d(Volume(colors.WHITE))

    def update(self, delta):
        
        # check for collisions
        for i in range(NUM_OBJECTS):
            for j in range(i+1, NUM_OBJECTS):
                o1 = self.objects_3d[i]
                o2 = self.objects_3d[j]
                if (o1.xneg() > o2.xneg() and o1.xneg() < o2.xpos) or (o1.xpos() > o2.xneg() and o1.xpos() < o2.xpos):
                    if (o1.yneg() > o2.yneg() and o1.yneg() < o2.ypos) or (o1.ypos() > o2.yneg() and o1.ypos() < o2.ypos):
                        if (o1.zneg() > o2.zneg() and o1.zneg() < o2.zpos) or (o1.zpos() > o2.zneg() and o1.zpos() < o2.zpos):
                            o1.reflect()
                            o2.reflect()
        
        # call the super class update method
        super(BruteForceScene, self).update(delta)

    def draw(self):
        # call the super class draw method
        super(BruteForceScene, self).draw()
