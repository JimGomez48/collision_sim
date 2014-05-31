from scene import Scene
import colors
from cube import Cube
from volume import Volume

from pprint import pprint

import random
random.seed()

NUM_OBJECTS = 15 # Number of objects in the scene

class SAPScene(Scene):
    def __init__(self):
        super(SAPScene, self).__init__()
        for i in range(NUM_OBJECTS):
            initxp = random.randint(-500,500)
            inityp = random.randint(-500,500)
            initzp = random.randint(-500,500)
            initxdv = random.randint(-1,1) - initxp/100
            initydv = random.randint(-1,1) - inityp/100
            initzdv = random.randint(-1,1) - initzp/100
            #self.add_object_3d(Ball(colors.BLUE, initxp, inityp, initzp, initxdv, initydv, initzdv))
            self.add_object_3d(Cube(colors.BLUE))
        self.add_object_3d(Volume(colors.WHITE))

    def update(self, delta):
        # call the super class update method
                
        #for x in self.objects_3d:
        #   pprint(vars(x))

        # get a list of the objects' X, Y and Z coordinates + its index and store it in PosList
        PosList = []
        for i in range(NUM_OBJECTS):
            PosListElement = []
            PosListElement.append(i)
            PosListElement.append(self.objects_3d[i].get_position()[0])
            PosListElement.append(self.objects_3d[i].get_position()[1])
            PosListElement.append(self.objects_3d[i].get_position()[2])
            PosList.append(PosListElement)

        #for x in PosList:
        #    print x

        

        # sort all objects

        # check for collisions
        # if so, react by changing their velocities

        super(SAPScene, self).update(delta)

    def draw(self):
        # call the super class draw method
        super(SAPScene, self).draw()