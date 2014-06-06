import random as rand
import numpy as np

from scene import Scene
from ball import *
from volume import Volume
from vector3 import *
import colors


class KdNode:
    def __init__(self, obj, axis, left, right):
        self.obj = obj
        self.axis = axis
        self.left = left
        self.right = right

    # def __str__(self):
    #     """
    #     print using in-order traversal
    #     """
    #     self.__in_order_print__(self)
    #
    # def __in_order_print__(self, node):
    #     """
    #     simple in-order traversal
    #     """
    #     if node is None:
    #         return
    #
    #     self.__in_order_print__(node.left)
    #     print node.obj.position()
    #     self.__in_order_print__(node.right)


def make_kd_tree(objs, dimensions=3, depth=0):
    """
    Recursively builds a KdTree

    :param objs: The object to store at this node
    :param dimensions: the number od dimensions to split along
    :param depth: the current depth of tree
    :return: a fully built KdTree
    """
    axis = depth % dimensions
    objs = sorted(objs, key=lambda obj: obj.position()[axis])
    median = len(objs) // 2

    if len(objs) == 0 or objs is None:
        return None

    return KdNode(
        obj=objs[median],
        axis=axis,
        left=make_kd_tree(objs[:median], dimensions, depth + 1),
        right=make_kd_tree(objs[median + 1:], dimensions, depth + 1),
    )


class KdTreeScene(Scene):
    def __init__(self, num_objects=50):
        super(KdTreeScene, self).__init__(num_objects)
        origin = Point3()
        for i in range(self.num_objects):
            position = Point3(
                rand.randint(-500, 500),
                rand.randint(-500, 500),
                rand.randint(-500, 500)
            )
            ball = CollidableBall(
                color=colors.BLUE,
                radius=30,
                mass=rand.randint(20, 100),
                start_p=position,
                start_v=Vector3(0, 0, rand.randint(200, 500))  # forward velocity
            )
            ball.update(1)  # force OM to update before turn_to_face
            ball.turn_to_face_p(origin)
            ball.rotate(5, Vector3(0, 1, 0))
            self.add_object_3d(ball)
        self.add_object_3d(Volume(colors.MAGENTA))
        self.kd_tree = make_kd_tree(self.objects_3d)

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
