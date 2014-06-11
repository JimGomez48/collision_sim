from scene import Scene
import colors
from ball import Ball
from volume import Volume

from sets import Set

import random
import sys
random.seed()

# NUM_OBJECTS = 25 # Number of objects in the scene

class SAPScene(Scene):

    xList = []
    yList = []
    zList = []

    def __init__(self, num_objects=50, sim_time=10):
        super(SAPScene, self).__init__(num_objects)

        # initialize fps & frames
        self.frame = 0
        self.fps_max = 0
        self.fps_min = 1000
        if sim_time is None:
            self.sim_time = 0
            self.SIM_TIME = 0
        else:
            self.sim_time = sim_time
            self.SIM_TIME = sim_time

        # set up objects in scene
        for i in range(self.num_objects):
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

        for i in range(self.num_objects):
            self.xList.append([i, self.objects_3d[i].xneg(), self.objects_3d[i].xpos()])
        
        for i in range(self.num_objects):
            self.yList.append([i, self.objects_3d[i].yneg(), self.objects_3d[i].ypos()])
        
        for i in range(self.num_objects):
            self.zList.append([i, self.objects_3d[i].zneg(), self.objects_3d[i].zpos()])

        #self.add_object_3d(Volume(colors.WHITE))
        
    def update(self, delta):
        
        # update sim statistics
        self.sim_time -= delta
        self.frame += 1
        fps = 1 / delta
        if fps > self.fps_max and self.frame > 3:
            self.fps_max = fps
        if fps < self.fps_min:
            self.fps_min = fps

        # perform collision checking
        self.collisionCheck()
        # call the super class update method
        super(SAPScene, self).update(delta)

        # if simulation is finished, print out info and exit
        if self.sim_time < 0 and self.SIM_TIME != 0:
            results_file = open("results_utkarsh.csv", "a")
            results_file.write(
                "%(name)s,%(a0)d,%(a1)d,%(a2)d,%(a3)f,%(a4)f,%(a5)d,%(a6)d\n" %
                {
                "name":("Sweep and Prune "),
                "a0": self.num_objects, "a1": self.SIM_TIME, "a2": self.frame,
                "a3": self.fps_min, "a4": self.fps_max, "a5": 0, "a6": 0
                }
            )
            results_file.close()
            exit()

    def collisionCheck(self):

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
        
        xPotentialCollisions = Set() # Potential collisions along x axis
        yPotentialCollisions = Set() # Potential collisions along y axis
        zPotentialCollisions = Set() # Potential collisions along z axis
        finalPotentialCollisions = Set() # Final list of potential collisions

        for i in range(self.num_objects):
            j = i-1
            while j >= 0 and self.xList[i][1] < self.xList[j][2]: # start of obj i < end of obj j implies they are colliding along X axis
                if tuple([self.xList[i][0], self.xList[j][0]]) not in xPotentialCollisions and tuple([self.xList[j][0], self.xList[i][0]]) not in xPotentialCollisions:
                    xPotentialCollisions.add(tuple([self.xList[i][0], self.xList[j][0]])) # append indices of potentially colliding objects
                j -= 1
            j = i+1
            while j < len(self.xList) and self.xList[i][2] > self.xList[j][1]: # end of obj i > start of obj j implies they are colliding along X axis
                if tuple([self.xList[i][0], self.xList[j][0]]) not in xPotentialCollisions and tuple([self.xList[j][0], self.xList[i][0]]) not in xPotentialCollisions:
                    xPotentialCollisions.add(tuple([self.xList[i][0], self.xList[j][0]])) # append indices of potentially colliding objects
                j += 1

        for i in range(self.num_objects):
            j = i-1
            while j >= 0 and self.yList[i][1] < self.yList[j][2]: # start of obj i < end of obj j implies they are colliding along Y axis
                if tuple([self.yList[i][0], self.yList[j][0]]) not in yPotentialCollisions and tuple([self.yList[j][0], self.yList[i][0]]) not in yPotentialCollisions:
                    yPotentialCollisions.add(tuple([self.yList[i][0], self.yList[j][0]])) # append indices of potentially colliding objects
                j -= 1
            j = i+1
            while j < len(self.yList) and self.yList[i][2] > self.yList[j][1]: # end of obj i > start of obj j implies they are colliding along Y axis
                if tuple([self.yList[i][0], self.yList[j][0]]) not in yPotentialCollisions and tuple([self.yList[j][0], self.yList[i][0]]) not in yPotentialCollisions:
                    yPotentialCollisions.add(tuple([self.yList[i][0], self.yList[j][0]])) # append indices of potentially colliding objects
                j += 1

        for i in range(self.num_objects):
            j = i-1
            while j >= 0 and self.zList[i][1] < self.zList[j][2]: # start of obj i < end of obj j implies they are colliding along Z axis
                if tuple([self.zList[i][0], self.zList[j][0]]) not in zPotentialCollisions and tuple([self.zList[j][0], self.zList[i][0]]) not in zPotentialCollisions:
                    zPotentialCollisions.add(tuple([self.zList[i][0], self.zList[j][0]])) # append indices of potentially colliding objects
                j -= 1
            j = i+1
            while j < len(self.zList) and self.zList[i][2] > self.zList[j][1]: # end of obj i > start of obj j implies they are colliding along Z axis
                if tuple([self.zList[i][0], self.zList[j][0]]) not in zPotentialCollisions and tuple([self.zList[j][0], self.zList[i][0]]) not in zPotentialCollisions:
                    zPotentialCollisions.add(tuple([self.zList[i][0], self.zList[j][0]])) # append indices of potentially colliding objects
                j += 1

        #print xPotentialCollisions, 'xPotentialCollisions'
        #print yPotentialCollisions, 'yPotentialCollisions'
        #print zPotentialCollisions, 'zPotentialCollisions'
        
        for x in xPotentialCollisions:
            if x in yPotentialCollisions and x in zPotentialCollisions:
                finalPotentialCollisions.add(x)

        #print finalPotentialCollisions, 'finalPotentialCollisions'

        # Adjust velocities of colliding objects
        for obj in finalPotentialCollisions:
            idx1 = obj[0]
            idx2 = obj[1]
            self.objects_3d[idx1].reflect()
            self.objects_3d[idx2].reflect()

    def draw(self):
        # call the super class draw method
        super(SAPScene, self).draw()