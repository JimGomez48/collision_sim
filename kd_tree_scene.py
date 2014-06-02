__author__ = 'james'

import random

from scene import Scene
from ball import Ball
from cube import Cube
from volume import Volume
from vector3 import *
import colors


class KdTreeScene(Scene):
    def __init__(self, num_objects=50):
        super(KdTreeScene, self).__init__(num_objects)
        for i in range(self.num_objects):
            position = Point3(
                random.randint(-700, 700),
                random.randint(-500, 500),
                random.randint(-500, 500)
            )
            cube = Cube(colors.CYAN, 50, position)
            self.add_object_3d(cube)
        self.add_object_3d(Volume(colors.WHITE))
        self.trans = Vector3(-1, -1, 1)
        self.rot_axis = Vector3(0, 1, 0)

    def update(self, delta):
        # call the super class update method
        # for o in self.objects_3d:
            # o.rotate(100 * delta, self.rot_axis)
            # o.translate_v(self.trans * delta)
        super(KdTreeScene, self).update(delta)

    def draw(self):
        # call the super class draw method
        super(KdTreeScene, self).draw()