from scene import Scene
import colors
from cube import Cube
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
            #self.add_object_3d(Ball(colors.BLUE, initxp, inityp, initzp, initxdv, initydv, initzdv))
            self.add_object_3d(Cube(colors.BLUE))

        # get a list of the objects' X, Y and Z coordinates + its index and store it in PosList
        for i in range(NUM_OBJECTS):
            PosListElement = []
            PosListElement.append(i)
            PosListElement.append(self.objects_3d[i].get_position()[0])
            PosListElement.append(self.objects_3d[i].get_position()[1])
            PosListElement.append(self.objects_3d[i].get_position()[2])
            self.PosList.append(PosListElement)

        # currently collecting start and end of AABB as position (x,y,z) +- side/2 instead of axial projections
        # store start and end of object boundaries along each axis, used to determine if collision is occurring

        for i in range(NUM_OBJECTS):
            xListElement = []
            xListElement.append(i)
            xListElement.append(self.objects_3d[i].get_position()[0] - self.objects_3d[i].side/2)
            xListElement.append(self.objects_3d[i].get_position()[0] + self.objects_3d[i].side/2)
            self.xList.append(xListElement)

        for i in range(NUM_OBJECTS):
            yListElement = []
            yListElement.append(i)
            yListElement.append(self.objects_3d[i].get_position()[1] - self.objects_3d[i].side/2)
            yListElement.append(self.objects_3d[i].get_position()[1] + self.objects_3d[i].side/2)
            self.yList.append(yListElement)
        
        for i in range(NUM_OBJECTS):
            zListElement = []
            zListElement.append(i)
            zListElement.append(self.objects_3d[i].get_position()[2] - self.objects_3d[i].side/2)
            zListElement.append(self.objects_3d[i].get_position()[2] + self.objects_3d[i].side/2)
            self.zList.append(zListElement)

        self.add_object_3d(Volume(colors.WHITE))
        
    def update(self, delta):
        
        # even though the lists are initialized by the constructor, they must be updated each time since object positions change

        # get a list of the objects' X, Y and Z coordinates + its index and store it in PosList
        for i in range(NUM_OBJECTS):
            PosListElement = []
            PosListElement.append(i)
            PosListElement.append(self.objects_3d[i].get_position()[0])
            PosListElement.append(self.objects_3d[i].get_position()[1])
            PosListElement.append(self.objects_3d[i].get_position()[2])
            self.PosList.append(PosListElement)

        # currently collecting start and end of AABB as position (x,y,z) +- side/2 instead of axial projections
        # store start and end of object boundaries along each axis, used to determine if collision is occurring

        for i in range(NUM_OBJECTS):
            xListElement = []
            xListElement.append(i)
            xListElement.append(self.objects_3d[i].get_position()[0] - self.objects_3d[i].side/2)
            xListElement.append(self.objects_3d[i].get_position()[0] + self.objects_3d[i].side/2)
            self.xList.append(xListElement)

        for i in range(NUM_OBJECTS):
            yListElement = []
            yListElement.append(i)
            yListElement.append(self.objects_3d[i].get_position()[1] - self.objects_3d[i].side/2)
            yListElement.append(self.objects_3d[i].get_position()[1] + self.objects_3d[i].side/2)
            self.yList.append(yListElement)
        
        for i in range(NUM_OBJECTS):
            zListElement = []
            zListElement.append(i)
            zListElement.append(self.objects_3d[i].get_position()[2] - self.objects_3d[i].side/2)
            zListElement.append(self.objects_3d[i].get_position()[2] + self.objects_3d[i].side/2)
            self.zList.append(zListElement)

        # sort all 3 lists based on the beginning positions of the AABBs
        self.xList.sort(key = lambda el: el[1])
        self.yList.sort(key = lambda el: el[1])
        self.zList.sort(key = lambda el: el[1])

        # check for collisions

        # if so, react by changing their velocities

        # call the super class update method
        super(SAPScene, self).update(delta)

    def draw(self):
        # call the super class draw method
        super(SAPScene, self).draw()