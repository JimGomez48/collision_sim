import random as rand

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
        self.dimensions = dimensions
        self.__root = self.__build_tree__(objs)

    def size(self):
        return self.__size

    def get_subtree(self, obj):
        """
        :param obj: the corresponding object of the node to be search
        :return: the subtree with the node containing obj as it's root
        """
        if obj is None:
            return None

        return self.__depth_first_search__(self.__root, obj)

    def __depth_first_search__(self, current_node, obj):
        if current_node.obj is obj:
            return current_node

        axis = current_node.axis
        if obj.position()[axis] < current_node.obj.position()[axis]:
            return self.__depth_first_search__(current_node.left, obj)
        else:
            return self.__depth_first_search__(current_node.right, obj)

    def __build_tree__(self, objs, depth=0):
        """
        Recursively builds a KdTree by splitting along the median node for each
        corresponding axis

        :param objs: The object to store at this node
        :param depth: the current depth of tree
        :return: a KdNode
        """
        axis = depth % self.dimensions
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
        self.kd_tree = KdTree(self.objects_3d, dimensions=3)
        self.check_for_collisions()
        super(KdTreeScene, self).update(delta)

    def draw(self):
        super(KdTreeScene, self).draw()

    def check_for_collisions(self):
        for o in self.objects_3d:
            subtree = self.kd_tree.get_subtree(o)
            if not subtree.left is None:
                depth_first_collision_check(subtree=subtree.left, test_obj=o)
            if not subtree.right is None:
                depth_first_collision_check(subtree=subtree.right, test_obj=o)


def depth_first_collision_check(subtree, test_obj):
    """
    Test test_obj for collisions against objects in the subtree

    :param subtree: the subtree of possible colliding objects
    :param test_obj: the object to test collision against
    """
    if subtree is None:
        return
    if test_obj.is_colliding(subtree.obj):
        test_obj.elastic_collide(subtree.obj)
    depth_first_collision_check(subtree.left, test_obj)
    depth_first_collision_check(subtree.right, test_obj)
