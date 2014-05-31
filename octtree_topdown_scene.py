from scene import Scene
import colors
from ball import Ball
from volume import Volume

import random
random.seed()

class OctTreeTopDownScene(Scene):
    def __init__(self):
        self.time = 0
        for i in range(10):
            initxp = random.randint(-500,500)
            inityp = random.randint(-500,500)
            initzp = random.randint(-500,500)
            initxdv = random.randint(-1,1) - initxp/100
            initydv = random.randint(-1,1) - inityp/100
            initzdv = random.randint(-1,1) - initzp/100
            self.add_object_3d(Ball(colors.BLUE, initxp, inityp, initzp, initxdv, initydv, initzdv))
        
        self.add_object_3d(Volume(colors.WHITE))
        super(OctTreeTopDownScene, self).__init__()
    
    def update(self, delta):
        #self.time += delta
        super(OctTreeTopDownScene, self).update(delta)

    def draw(self):
        # call the super class draw method
        super(OctTreeTopDownScene, self).draw()
