__author__ = 'james'

from scene import Scene
import colors
from ball import Ball
from cube import Cube
from volume import Volume


class OctTreeBottomUpScene(Scene):
    def __init__(self):
        super(OctTreeBottomUpScene, self).__init__()
        for i in range(20):
            self.add_object_3d(Cube(colors.YELLOW))
        self.add_object_3d(Volume(colors.WHITE))

    def update(self, delta):
        # call the super class update method
        super(OctTreeBottomUpScene, self).update(delta)

    def draw(self):
        # call the super class draw method
        super(OctTreeBottomUpScene, self).draw()