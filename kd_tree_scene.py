import random as rand
import numpy as np

from scene import Scene
from ball import *
from volume import Volume
from vector3 import *
import colors


class KdTree:
    __root = None
    __size = 0

    class KdNode:
        def __init__(self, obj, axis, left, right):
            self.obj = obj
            self.axis = axis
            self.left = left
            self.right = right

    def __init__(self, objs, dimensions=3):
        self.dims = dimensions
        self.__root = self.__build_tree__(objs)

    def size(self):
        return self.__size

    def __build_tree__(self, objs, depth=0):
        """
        Recursively builds a KdTree by splitting along the median node for each
        corresponding axis

        :param objs: The object to store at this node
        :param depth: the current depth of tree
        :return: a KdNode
        """
        axis = depth % self.dims
        objs = sorted(objs, key=lambda obj: obj.position()[axis])
        median = len(objs) // 2

        if len(objs) == 0 or objs is None:
            return None

        self.__size += 1
        return self.KdNode(
            obj=objs[median],
            axis=axis,
            left=self.__build_tree__(objs[:median], depth + 1),
            right=self.__build_tree__(objs[median + 1:], depth + 1),
        )


def depth_first_collision_check(node, test_obj):
    if node is None:
        return

    if test_obj.is_colliding(node.obj):
        test_obj.elastic_collide(node.obj)
    depth_first_collision_check(node.left, test_obj)
    depth_first_collision_check(node.right, test_obj)


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
        # self.add_object_3d(Volume(colors.MAGENTA))
        self.kd_tree = KdTree(self.objects_3d, dimensions=3)
        print str(self.kd_tree.size())

    def update(self, delta):
        # call the super class update method
        self.kd_tree = KdTree(self.objects_3d, dimensions=3)
        # self.check_for_collisions()
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

        # already_collided = set([])
        # for i in range(self.num_objects):
        #     o1 = self.objects_3d[i]
        #     assert isinstance(o1, CollidableBall)
            # for j in range(i + 1, self.num_objects):
            #     o2 = self.objects_3d[j]
            #     assert isinstance(o2, CollidableBall)
                # if o1.is_colliding(o2):
                #     if not i in already_collided:
                #         already_collided.add(i)
                #         if not j in already_collided:
                #             already_collided.add(j)
                #             o1.elastic_collide(o2)

        for o in self.objects_3d:
            current_node = self.kd_tree
            while not current_node.obj is o:  # search tree until matching node found
                if current_node is None:
                    raise StandardError(
                        "Object not in KD tree. Something is wrong!")
                axis = current_node.axis
                if o.position()[axis] < current_node.obj.position()[axis]:
                    current_node = current_node.left
                else:
                    current_node = current_node.right
            # Found the matching node. Now check subtree against o
            depth_first_collision_check(node=current_node, test_obj=o)