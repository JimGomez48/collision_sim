from scene import Scene
import colors
from cube import Cube
from ball import Ball
from volume import Volume

from pprint import pprint

import random
random.seed()

NUM_OBJECTS = 10 # Number of objects in the scene
OCTREE_MAX_SIZE = 10000
OCTREE_LEVELS = 2

class OctreeNode:
    xpypzp, xpypzn, xpynzp, xpynzn, xnypzp, xnypzn, xnynzp, xnynzn = None, None, None, None, None, None, None, None
    objs = []
    
    def fill_octree(self, xmax, xmin, ymax, ymin, zmax, zmin, levels):
        if levels == 0:
            return
    
        for o in self.objs:
            xmid = (xmax+xmin)/2
            ymid = (ymax+ymin)/2
            zmid = (zmax+zmin)/2
            
            if o.xpos > xmid and o.ypos > ymid and o.zpos > zmid:
                add_obj_xpypzp(o)
            
            if o.xpos > xmid and o.ypos > ymid and o.zneg < zmid:
                add_obj_xpypzn(o)
            
            if o.xpos > xmid and o.yneg < ymid and o.zpos > zmid:
                add_obj_xpynzp(o)
            
            if o.xpos > xmid and o.yneg < ymid and o.zneg < zmid:
                add_obj_xpynzn(o)
            
            if o.xneg < xmid and o.ypos > ymid and o.zpos > zmid:
                add_obj_xnypzp(o)
            
            if o.xneg < xmid and o.ypos > ymid and o.zneg < zmid:
                add_obj_xnypzn(o)
            
            if o.xneg < xmid and o.yneg < ymid and o.zpos > zmid:
                add_obj_xnynzp(o)
            
            if o.xneg < xmid and o.yneg < ymid and o.zneg < zmid:
                add_obj_xnynzn(o)
        
        if self.xpypzp != None:
            self.xpypzp.fill_octree(xmax, xmid, ymax, ymid, zmax, zmid, levels-1)
        if self.xpypzn != None:
            self.xpypzn.fill_octree(xmax, xmid, ymax, ymid, zmid, zmin, levels-1)
        if self.xpynzp != None:
            self.xpynzp.fill_octree(xmax, xmid, ymid, ymin, zmax, zmid, levels-1)
        if self.xpynzn != None:
            self.xpynzn.fill_octree(xmax, xmid, ymid, ymin, zmid, zmin, levels-1)
        if self.xnypzp != None:
            self.xnypzp.fill_octree(xmid, xmin, ymax, ymid, zmax, zmid, levels-1)
        if self.xnypzn != None:
            self.xnypzn.fill_octree(xmid, xmin, ymax, ymid, zmid, zmin, levels-1)
        if self.xnynzp != None:
            self.xnynzp.fill_octree(xmid, xmin, ymad, ymin, zmax, zmid, levels-1)
        if self.xnynzn != None:
            self.xnynzn.fill_octree(xmid, xmin, ymad, ymin, zmid, zmin, levels-1)
    
    def add_obj_xpypzp(self, obj):
        if xpypzp == None:
            xpypzp = OctreeNode()
        xpypzp.objs.append(obj)
    
    def add_obj_xpypzn(self, obj):
        if xpypzn == None:
            xpypzn = OctreeNode()
        xpypzn.objs.append(obj)
    
    def add_obj_xpynzp(self, obj):
        if xpynzp == None:
            xpynzp = OctreeNode()
        xpynzp.objs.append(obj)
    
    def add_obj_xpynzn(self, obj):
        if xpynzn == None:
            xpynzn = OctreeNode()
        xpynzn.objs.append(obj)
    
    def add_obj_xnypzp(self, obj):
        if xnypzp == None:
            xnypzp = OctreeNode()
        xnypzp.objs.append(obj)
    
    def add_obj_xnypzn(self, obj):
        if xnypzn == None:
            xnypzn = OctreeNode()
        xnypzn.objs.append(obj)
    
    def add_obj_xnynzp(self, obj):
        if xnynzp == None:
            xnynzp = OctreeNode()
        xnynzp.objs.append(obj)
    
    def add_obj_xnynzn(self, obj):
        if xnynzn == None:
            xnynzn = OctreeNode()
        xnynzn.objs.append(obj)
    
    
class OctTreeTopDownScene(Scene):

    PosList = xList = yList = zList = []
    def __init__(self):
        super(OctTreeTopDownScene, self).__init__()
        
        for i in range(NUM_OBJECTS):
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
        
        #Create and fill Octree
        octree_root = OctreeNode()
        
        for o in self.objects_3d:
            if o.xpos > -OCTREE_MAX_SIZE and o.xneg < OCTREE_MAX_SIZE and o.ypos > -OCTREE_MAX_SIZE and o.yneg < OCTREE_MAX_SIZE and o.zpos > -OCTREE_MAX_SIZE and o.zneg < OCTREE_MAX_SIZE:
                octree_root.objs.append( o )
        
        octree_root.fill_octree(OCTREE_MAX_SIZE, -OCTREE_MAX_SIZE, OCTREE_MAX_SIZE, -OCTREE_MAX_SIZE, OCTREE_MAX_SIZE, -OCTREE_MAX_SIZE, OCTREE_LEVELS)
                
        # check for collisions
        for i in range(NUM_OBJECTS):
            for j in range(i+1, NUM_OBJECTS):
                if self.collides(i,j):
                    self.objects_3d[i].reflect()
                    self.objects_3d[j].reflect()
        
        # call the super class update method
        super(OctTreeTopDownScene, self).update(delta)
    
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
        super(OctTreeTopDownScene, self).draw()

