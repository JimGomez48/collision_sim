__author__ = 'james'

import random

from scene import Scene
from ball import *
from volume import Volume
from vector3 import *
import colors


class KdTreeScene(Scene):
    def __init__(self, num_objects=50):
        super(KdTreeScene, self).__init__(num_objects)
        origin = Point3()
        for i in range(self.num_objects):
            position = Point3(
                random.randint(-700, 700),
                random.randint(-500, 500),
                random.randint(-500, 500)
            )
            ball = CollidableBall(colors.DARK_BLUE, 40, position, Vector3(0, 0, 300))
            ball.update(1) # force OM to update before turn_to_face
            ball.turn_to_face_p(origin)
            self.add_object_3d(ball)
        self.add_object_3d(Volume(colors.MAGENTA))

    def update(self, delta):
        # call the super class update method
        for o in self.objects_3d:
            # o.rotate(100 * delta, self.rot_axis)
            o.update(delta)
        super(KdTreeScene, self).update(delta)

    def draw(self):
        # call the super class draw method
        super(KdTreeScene, self).draw()