import random

from scene import Scene
from ball import *
from volume import Volume
from vector3 import *
import colors


class KdTreeNode:
    def __init__(self, position=Point3()):
        self.position = position
        self.left = None
        self.right = None
        self.children = []
        # TODO everything else

class KdTreeScene(Scene):
    def __init__(self, num_objects=50):
        super(KdTreeScene, self).__init__(num_objects)
        origin = Point3()
        for i in range(self.num_objects):
            position = Point3(
                random.randint(-500, 500),
                random.randint(-500, 500),
                random.randint(-500, 500)
            )
            ball = CollidableBall(
                color=colors.BLUE,
                radius=30,
                mass=random.randint(20, 100),
                start_p=position,
                start_v=Vector3(0, 0, random.randint(200, 500))  # forward velocity
            )
            ball.update(1)  # force OM to update before turn_to_face
            ball.turn_to_face_p(origin)
            ball.rotate(5, Vector3(0, 1, 0))
            self.add_object_3d(ball)
        self.add_object_3d(Volume(colors.MAGENTA))

    def update(self, delta):
        # call the super class update method
        self.check_for_collisions()
        for o in self.objects_3d:
            # o.rotate(100 * delta, self.rot_axis)
            o.update(delta)
        super(KdTreeScene, self).update(delta)

    def draw(self):
        # call the super class draw method
        super(KdTreeScene, self).draw()

    def check_for_collisions(self):
        # already_collided = set([])
        # for i in range(self.num_objects):
        #     for j in range(i + 1, self.num_objects):
        #         if self.collides(i, j):
        #             if not i in already_collided:
        #                 self.objects_3d[i].reflect()
        #                 already_collided.add(i)
        #
        #             if not j in already_collided:
        #                 self.objects_3d[j].reflect()
        #                 already_collided.add(j)

        already_collided = set([])
        for i in range(self.num_objects):
            o1 = self.objects_3d[i]
            # assert isinstance(o1, CollidableBall)
            for j in range(i + 1, self.num_objects):
                o2 = self.objects_3d[j]
                # assert isinstance(o2, CollidableBall)
                if o1.is_colliding(o2):
                    if not i in already_collided:
                        already_collided.add(i)
                        if not j in already_collided:
                            already_collided.add(j)
                            o1.elastic_collide(o2)
