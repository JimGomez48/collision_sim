from scene import Scene
import colors
from cube import Cube
from ball import Ball
from volume import Volume
import copy
from pprint import pprint

import random
random.seed()

# NUM_OBJECTS = 512 # Number of objects in the scene, O(N)
OCTREE_MAX_SIZE = 300 #Maximum size of the octree root, in pixels, O(M)
OCTREE_LEVELS = 6 # Number of levels in the octree, O(L)
BALL_VELOCITY = 5

class OctreeNode:
    def __init__(self):
        self.xpypzp, self.xpypzn, self.xpynzp, self.xpynzn, self.xnypzp, self.xnypzn, self.xnynzp, self.xnynzn = None, None, None, None, None, None, None, None
        self.objs = set([])
    
    def get_leaves_inter(self): #OMEGA(N)
        #print "GET LEAVES"
        if not self.xpypzp and not self.xpypzn and not self.xpynzp and not self.xpynzn and not self.xnypzp and not self.xnypzn and not self.xnynzp and not self.xnynzn:
            if len(self.objs) > 1:
                #print str(len(self.objs)) + " objects colliding"
                return self.objs
            else:
                return []
        
        leaves = []
        
        if self.xpypzp:
            leaves.extend( self.xpypzp.get_leaves_inter() )
        if self.xpypzn:
            leaves.extend( self.xpypzn.get_leaves_inter() )
        if self.xpynzp:
            leaves.extend( self.xpynzp.get_leaves_inter() )
        if self.xpynzn:
            leaves.extend( self.xpynzn.get_leaves_inter() )
        if self.xnypzp:
            leaves.extend( self.xnypzp.get_leaves_inter() )
        if self.xnypzn:
            leaves.extend( self.xnypzn.get_leaves_inter() )
        if self.xnynzp:
            leaves.extend( self.xnynzp.get_leaves_inter() )
        if self.xnynzn:
            leaves.extend( self.xnynzn.get_leaves_inter() )
        
        return leaves
    
    def get_leaves(self): #OMEGA(N)
        #print "GET LEAVES"
        if not self.xpypzp and not self.xpypzn and not self.xpynzp and not self.xpynzn and not self.xnypzp and not self.xnypzn and not self.xnynzp and not self.xnynzn:
            return [self.objs]
        
        leaves = []
        
        if self.xpypzp:
            leaves.append( self.xpypzp.get_leaves_inter() )
        if self.xpypzn:
            leaves.append( self.xpypzn.get_leaves_inter() )
        if self.xpynzp:
            leaves.append( self.xpynzp.get_leaves_inter() )
        if self.xpynzn:
            leaves.append( self.xpynzn.get_leaves_inter() )
        if self.xnypzp:
            leaves.append( self.xnypzp.get_leaves_inter() )
        if self.xnypzn:
            leaves.append( self.xnypzn.get_leaves_inter() )
        if self.xnynzp:
            leaves.append( self.xnynzp.get_leaves_inter() )
        if self.xnynzn:
            leaves.append( self.xnynzn.get_leaves_inter() )
        
        return leaves
    
    
    def fill_octree(self, xmax, xmin, ymax, ymin, zmax, zmin, levels): #OMEGA(L*N)
        #print "FILL OCTREE"
        if levels == 0 or len(self.objs) <= 1:
            return
        
        for o in self.objs:
            #print str(levels) + " " + str(self.objs.index(o)) + " " + str( len(self.objs) )
            xmid = (xmax+xmin)/2
            ymid = (ymax+ymin)/2
            zmid = (zmax+zmin)/2
            
            if o.xpos() >= xmid and o.ypos() >= ymid and o.zpos() >= zmid:
                self.add_obj_xpypzp(o)
            
            if o.xpos() >= xmid and o.ypos() >= ymid and o.zneg() <= zmid:
                self.add_obj_xpypzn(o)
            
            if o.xpos() >= xmid and o.yneg() <= ymid and o.zpos() >= zmid:
                self.add_obj_xpynzp(o)
            
            if o.xpos() >= xmid and o.yneg() <= ymid and o.zneg() <= zmid:
                self.add_obj_xpynzn(o)
            
            if o.xneg() <= xmid and o.ypos() >= ymid and o.zpos() >= zmid:
                self.add_obj_xnypzp(o)
            
            if o.xneg() <= xmid and o.ypos() >= ymid and o.zneg() <= zmid:
                self.add_obj_xnypzn(o)
            
            if o.xneg() <= xmid and o.yneg() <= ymid and o.zpos() >= zmid:
                self.add_obj_xnynzp(o)
            
            if o.xneg() <= xmid and o.yneg() <= ymid and o.zneg() <= zmid:
                self.add_obj_xnynzn(o)
        
        
        if self.xpypzp:
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
            self.xnynzp.fill_octree(xmid, xmin, ymid, ymin, zmax, zmid, levels-1)
        if self.xnynzn != None:
            self.xnynzn.fill_octree(xmid, xmin, ymid, ymin, zmid, zmin, levels-1)
    
    def add_obj_xpypzp(self, obj):
        if self.xpypzp == None:
            self.xpypzp = OctreeNode()
        if not obj in self.xpypzp.objs:
            self.xpypzp.objs.add(obj)
    
    def add_obj_xpypzn(self, obj):
        if self.xpypzn == None:
            self.xpypzn = OctreeNode()
        if not obj in self.xpypzn.objs:
            self.xpypzn.objs.add(obj)
    
    def add_obj_xpynzp(self, obj):
        if self.xpynzp == None:
            self.xpynzp = OctreeNode()
        if not obj in self.xpynzp.objs:
            self.xpynzp.objs.add(obj)
    
    def add_obj_xpynzn(self, obj):
        if self.xpynzn == None:
            self.xpynzn = OctreeNode()
        if not obj in self.xpynzn.objs:
            self.xpynzn.objs.add(obj)
    
    def add_obj_xnypzp(self, obj):
        if self.xnypzp == None:
            self.xnypzp = OctreeNode()
        if not obj in self.xnypzp.objs:
            self.xnypzp.objs.add(obj)
    
    def add_obj_xnypzn(self, obj):
        if self.xnypzn == None:
            self.xnypzn = OctreeNode()
        if not obj in self.xnypzn.objs:
            self.xnypzn.objs.add(obj)
    
    def add_obj_xnynzp(self, obj):
        if self.xnynzp == None:
            self.xnynzp = OctreeNode()
        if not obj in self.xnynzp.objs:
            self.xnynzp.objs.add(obj)
    
    def add_obj_xnynzn(self, obj):
        if self.xnynzn == None:
            self.xnynzn = OctreeNode()
        if not obj in self.xnynzn.objs:
            self.xnynzn.objs.add(obj)
    

class OctTreeAltScene(Scene):
    
    PosList = xList = yList = zList = []
    def __init__(self, num_objects=50):
        super(OctTreeAltScene, self).__init__(num_objects)
        
        self.fps_max = 0
        self.fps_min = 1000
        self.compared_min = self.num_objects ** 2
        self.compared_max = 0
        self.frame = 0
        
        for i in range(self.num_objects):
            while 1 == 1:
                
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
        
        #Create and fill Octree
        octree_root = None
        octree_root = OctreeNode()
        
        for o in self.objects_3d:
            if o.xpos() > -OCTREE_MAX_SIZE and o.xneg() < OCTREE_MAX_SIZE and o.ypos() > -OCTREE_MAX_SIZE and o.yneg() < OCTREE_MAX_SIZE and o.zpos() > -OCTREE_MAX_SIZE and o.zneg() < OCTREE_MAX_SIZE:
                octree_root.objs.add( o )
        
        octree_root.fill_octree(OCTREE_MAX_SIZE, -OCTREE_MAX_SIZE, OCTREE_MAX_SIZE, -OCTREE_MAX_SIZE, OCTREE_MAX_SIZE, -OCTREE_MAX_SIZE, OCTREE_LEVELS)
        
        # check for collisions        
        already_collided = set([])
        #print "Leaves: " + str(len(octree_root.get_leaves()))
        num_of_leaves = 0
        for l in octree_root.get_leaves():
            if len(l) > 1:
                num_of_leaves += len(l)
                #print "    Subleaves: " + str(len(l))
                for o in l:
                    if not o in already_collided:
                        #print "        Ball " + str( self.objects_3d.index(o) ) + " collided"
                        already_collided.add( o )
                        o.reflect()
                    #else:
                        #print "        Ball " + str( self.objects_3d.index(o) ) + " in list already"
                        
        if num_of_leaves < self.compared_min and self.frame > 3:
            self.compared_min = num_of_leaves
            
        if num_of_leaves > self.compared_max:
            self.compared_max = num_of_leaves
        
        print "Collisions: " + '%-4s'%str(len(already_collided)) + "    Objects compared: " + '%-5s'%str(num_of_leaves) + "    Min: " + '%-5s'%str(self.compared_min) + "   Max: " + str(self.compared_max)
        #print "FPS: " + '%-3s'%str(fps) + "    MIN: " + str(self.fps_min) + "    MAX: " + str(self.fps_max)
        # call the super class update method
        super(OctTreeAltScene, self).update(delta)
    
    def collides_obj(self, o1,o2):
        if o1==o2:
            return 0
        
        if (o1.xneg() > o2.xneg() and o1.xneg() < o2.xpos()) or (o1.xpos() > o2.xneg() and o1.xpos() < o2.xpos()):
            if (o1.yneg() > o2.yneg() and o1.yneg() < o2.ypos()) or (o1.ypos() > o2.yneg() and o1.ypos() < o2.ypos()):
                if (o1.zneg() > o2.zneg() and o1.zneg() < o2.zpos()) or (o1.zpos() > o2.zneg() and o1.zpos() < o2.zpos()):
                    return 1
        return 0
    
    def collides(self, i,j):
        if i==j:
            return 0
        
        o1 = self.objects_3d[i]
        o2 = self.objects_3d[j]
        if (o1.xneg() > o2.xneg() and o1.xneg() < o2.xpos()) or (o1.xpos() > o2.xneg() and o1.xpos() < o2.xpos()):
            if (o1.yneg() > o2.yneg() and o1.yneg() < o2.ypos()) or (o1.ypos() > o2.yneg() and o1.ypos() < o2.ypos()):
                if (o1.zneg() > o2.zneg() and o1.zneg() < o2.zpos()) or (o1.zpos() > o2.zneg() and o1.zpos() < o2.zpos()):
                    return 1
        return 0
    
    def draw(self):
        # call the super class draw method
        super(OctTreeAltScene, self).draw()
