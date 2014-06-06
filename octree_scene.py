from scene import Scene
import colors
from cube import Cube
from ball import Ball
from volume import Volume
import copy
from pprint import pprint

import random
random.seed()

OCTREE_MAX_SIZE = 300 #Maximum size of the octree root, in pixels, O(M)

class OctreeNode:
    def __init__(self):
        self.xpypzp, self.xpypzn, self.xpynzp, self.xpynzn, self.xnypzp, self.xnypzn, self.xnynzp, self.xnynzn = None, None, None, None, None, None, None, None
        self.objs = set([])
    
    def get_leaves_inter(self):
        if not self.xpypzp and not self.xpypzn and not self.xpynzp and not self.xpynzn and not self.xnypzp and not self.xnypzn and not self.xnynzp and not self.xnynzn:
            if len(self.objs) > 1:
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
    
    def get_leaves(self):
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
    
    
    def fill_octree(self, xmax, xmin, ymax, ymin, zmax, zmin, levels):
        if levels == 0 or len(self.objs) <= 1:
            return
        
        for o in self.objs:
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
    

class OctreeScene(Scene):
    
    PosList = xList = yList = zList = []
    def __init__(self, num_objects=50, octree_levels=5, sim_time=10):
        super(OctreeScene, self).__init__(num_objects)
        
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
        
        #Initialize octree parameters
        self.compared_min = num_objects ** 2
        self.compared_max = 0
        
        self.octree_levels = octree_levels
        if octree_levels == None:
            self.octree_levels = 5
        
        #Initialize scene objects
        for i in range(num_objects):
            while 1==1:
                
                #Create randomly positioned ball
                initxp = random.randint(-500,500)
                inityp = random.randint(-500,500)
                initzp = random.randint(-500,500)
                initxdv = random.randint(-2,2) - initxp/25
                initydv = random.randint(-2,2) - inityp/25
                initzdv = random.randint(-2,2) - initzp/25
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
        
        #Create and fill Octree
        octree_root = None
        octree_root = OctreeNode()
        
        ot_max_x = ot_min_x = ot_max_y = ot_min_y = ot_max_z = ot_min_z = 0
        for o in self.objects_3d:
            if o.xpos() > ot_max_x:
                ot_max_x = o.xpos()
            if o.xneg() < ot_min_x:
                ot_min_x = o.xneg()
            if o.ypos() > ot_max_y:
                ot_max_y = o.ypos()
            if o.yneg() < ot_min_y:
                ot_min_y = o.yneg()
            if o.zpos() > ot_max_z:
                ot_max_z = o.zpos()
            if o.zneg() < ot_min_z:
                ot_min_z = o.zneg()
        
        for o in self.objects_3d:
            octree_root.objs.add( o )
        
        octree_root.fill_octree(ot_max_x, ot_min_x, ot_max_y, ot_min_y, ot_max_z, ot_min_z, self.octree_levels)
        
        # check for collisions        
        already_collided = set([])
        num_of_leaves = 0
        for l in octree_root.get_leaves():
            if len(l) > 1:
                num_of_leaves += len(l)
                for o in l:
                    if not o in already_collided:
                        already_collided.add( o )
                        for o2 in already_collided:
                            if self.collides_obj(o, o2):
                                o.reflect()
                                o2.reflect()
                        
        if num_of_leaves < self.compared_min and self.frame > 3:
            self.compared_min = num_of_leaves
            
        if num_of_leaves > self.compared_max:
            self.compared_max = num_of_leaves
        
        #If simulation is finished, print out info
        if self.sim_time < 0 and self.SIM_TIME != 0:
            results_file = open("results.csv", "a")
            results_file.write("%(name)s,%(a0)d,%(a1)d,%(a2)d,%(a3)f,%(a4)f,%(a5)d,%(a6)d\n"%
                {"name":("Octree " + str(self.octree_levels) + " Levels"),"a0":self.num_objects, "a1":self.SIM_TIME, "a2":self.frame, "a3":self.fps_min, "a4":self.fps_max, "a5":self.compared_min, "a6":self.compared_max})
            results_file.close()
            exit()
    
        
        # call the super class update method
        super(OctreeScene, self).update(delta)
        
        
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
        super(OctreeScene, self).draw()

