from scene import Scene
import colors
from cube import Cube
from ball import Ball
from volume import Volume

from pprint import pprint

import random
random.seed()

# NUM_OBJECTS = 500 # Number of objects in the scene

class NoCollisionsScene(Scene):

    PosList = xList = yList = zList = []
    def __init__(self, num_objects=50, sim_time = 10):
        super(NoCollisionsScene, self).__init__(num_objects)
        
        #Initialize fps & frames
        self.frame = 0
        self.fps_max = 0
        self.fps_min = 1000
        
        if sim_time == None:
            self.sim_time = 0
            self.SIM_TIME = 0
        else:
            self.sim_time = sim_time
            self.SIM_TIME = sim_time
        
        #Initialize scene objects
        for i in range(num_objects):
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
        #Update fps & frames
        self.sim_time -= delta
        self.frame += 1
        fps = 1/delta
        if fps > self.fps_max and self.frame > 3:
            self.fps_max = fps
                
        if fps < self.fps_min:
            self.fps_min = fps
        
        #If simulation is finished, print out info
        if self.sim_time < 0 and self.SIM_TIME != 0:
            results_file = open("results.csv", "a")
            results_file.write("%(name)s,%(a0)d,%(a1)d,%(a2)d,%(a3)f,%(a4)f,%(a5)d,%(a5)d\n"%
                {"name":("No Collisions"),"a0":self.num_objects, "a1":self.SIM_TIME, "a2":self.frame, "a3":self.fps_min, "a4":self.fps_max, "a5":0})
            results_file.close()
            exit()
        
        # call the super class update method
        super(NoCollisionsScene, self).update(delta)
    
    
    def draw(self):
        # call the super class draw method
        super(NoCollisionsScene, self).draw()
