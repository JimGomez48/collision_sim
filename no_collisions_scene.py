from scene import Scene
import colors
from cube import Cube
from ball import Ball
from volume import Volume

from pprint import pprint

import random
random.seed()

NUM_OBJECTS = 500 # Number of objects in the scene

class NoCollisionsScene(Scene):

    PosList = xList = yList = zList = []
    def __init__(self):
        super(NoCollisionsScene, self).__init__()
        
        for i in range(NUM_OBJECTS):
            #Create randomly positioned ball
            initxp = random.randint(-500,500)
            inityp = random.randint(-500,500)
            initzp = random.randint(-500,500)
            initxdv = random.randint(-2,2) - initxp/50
            initydv = random.randint(-2,2) - inityp/50
            initzdv = random.randint(-2,2) - initzp/50
            self.add_object_3d(Ball(colors.BLUE, initxp, inityp, initzp, initxdv, initydv, initzdv))
    
    def printinfo(self, i):
        return "(" + str(self.objects_3d[i].xp) + " " + str(self.objects_3d[i].yp) + " " + str(self.objects_3d[i].zp) + ") (" + str(self.objects_3d[i].xv) + " " + str(self.objects_3d[i].yv) + " " + str(self.objects_3d[i].zv) + ")"
    
    def update(self, delta):
        # call the super class update method
        super(NoCollisionsScene, self).update(delta)
    
    def draw(self):
        # call the super class draw method
        super(NoCollisionsScene, self).draw()
