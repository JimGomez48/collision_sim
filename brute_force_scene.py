from scene import Scene
import colors
from cube import Cube
from ball import Ball
from volume import Volume

from pprint import pprint

import random
random.seed()

# NUM_OBJECTS = 512 # Number of objects in the scene

class BruteForceScene(Scene):

    PosList = xList = yList = zList = []
    def __init__(self, num_objects=50, sim_time=10):
        super(BruteForceScene, self).__init__(num_objects)
        
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
            while 1==1:
                #Create randomly positioned ball
                initxp = random.randint(-500,500)
                inityp = random.randint(-500,500)
                initzp = random.randint(-500,500)
                initxdv = random.randint(-2,2) - initxp/50
                initydv = random.randint(-2,2) - inityp/50
                initzdv = random.randint(-2,2) - initzp/50
                self.add_object_3d(Ball(colors.BLUE, initxp, inityp, initzp, initxdv, initydv, initzdv))
                
                #Ensure no collisions with other balls
                flag_coll = 0
                for j in range(i-1):
                    if self.collides(i,j):
                        self.remove_last_object_3d()
                        break
                else:
                    #This is only executed if the j-for-loop exits normally, e.g. no collisions. Otherwise the infinite while will continue.
                    break
    
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
        
        # check for collisions
        already_collided = set([])
        for i in range(self.num_objects):
            for j in range(i+1, self.num_objects):
                if self.collides(i,j):
                    if not i in already_collided:
                        self.objects_3d[i].reflect()
                        already_collided.add(i)
                    
                    if not j in already_collided:
                        self.objects_3d[j].reflect()
                        already_collided.add(j)
        
        #If simulation is finished, print out info
        if self.sim_time < 0 and self.SIM_TIME != 0:
            results_file = open("results.csv", "a")
            results_file.write("%(name)s,%(a0)d,%(a1)d,%(a2)d,%(a3)f,%(a4)f,%(a5)d,%(a5)d\n"%
                {"name":("Brute Force"),"a0":self.num_objects, "a1":self.SIM_TIME, "a2":self.frame, "a3":self.fps_min, "a4":self.fps_max, "a5":self.num_objects ** 2})
            results_file.close()
            exit()
        
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
