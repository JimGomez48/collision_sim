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
    def __init__(self, num_objects=50):
        super(BruteForceScene, self).__init__(num_objects)
        self.fps_max = 0
        self.fps_min = 1000
        self.frame = 0
        
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
        self.frame += 1
        fps = int(1/delta)
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
        
        print "Collisions: " + '%-3s'%str(len(already_collided)) + "    Objects compared: " + str(self.num_objects ** 2)
        #print "FPS: " + '%-3s'%str(fps) + "    MIN: " + str(self.fps_min) + "    MAX: " + str(self.fps_max)
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
