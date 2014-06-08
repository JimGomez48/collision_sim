import sys
import random as rand

from scene import Scene
from ball import *
from vector3 import *
import colors


class KdTree:
    __root = None
    __size = 0

    class KdNode:
        def __init__(self, obj, axis, depth, left, right):
            self.obj = obj
            self.axis = axis
            self.depth = depth
            self.left = left
            self.right = right

        def __str__(self):
            return self.obj.position().__str__() + " axis: " + str(self.axis)

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
            raise ArgumentError("obj cannot be None")

        return self.__depth_first_search__(self.__root, obj)

    def height(self):
        return self.__height_recursive__(self.__root) - 1

    def print_tree(self):
        print "K-D Tree:"
        self.__print_recursive__(self.__root)
        print "SIZE: " + str(self.size())
        print "HEIGHT: " + str(self.height())
        print

    def __print_recursive__(self, node, indent=0):
        space = ""
        for i in range(indent):
            space += "    "
        print space + str(node.__str__())

        if not node is None:
            if not node.left is None:
                self.__print_recursive__(node.left, indent + 1)
            if not node.right is None:
                self.__print_recursive__(node.right, indent + 1)

    def __depth_first_search__(self, current_node, obj):
        try:
            if current_node.obj.position() == obj.position():
                return current_node

            axis = current_node.axis
            # print str(current_node)
            if obj.position()[axis] < current_node.obj.position()[axis]:
                # print str(obj.position()[axis]) + " < " + \
                #       str(current_node.obj.position()[axis])
                # print "left"
                return self.__depth_first_search__(current_node.left, obj)
            else:
                # print str(obj.position()[axis]) + " >= " + \
                #       str(current_node.obj.position()[axis])
                # print "right"
                return self.__depth_first_search__(current_node.right, obj)
        except AttributeError as e:
            sys.stderr("\nDidn't find Search-Node " + str(obj.position()))
            self.print_tree()
            exit()

    def __height_recursive__(self, node):
        if node is None:
            return 0

        left_height = self.__height_recursive__(node.left)
        right_height = self.__height_recursive__(node.right)

        if left_height > right_height:
            return left_height + 1
        else:
            return right_height + 1

    def __build_tree__(self, objs, depth=0):
        """
        Recursively builds a KdTree by splitting along the median node for each
        corresponding axis

        :param objs: The object to store at this node
        :param depth: the current depth of tree
        :return: a KdNode
        """
        if len(objs) == 0 or objs is None:
            return None

        axis = depth % self.dimensions
        objs = sorted(objs, key=lambda obj: obj.position()[axis])
        median = self.__get_adjusted_median__(objs, axis)
        self.__size += 1

        return self.KdNode(
            obj=objs[median],
            axis=axis,
            depth=depth,
            left=self.__build_tree__(objs[:median], depth + 1),
            right=self.__build_tree__(objs[median + 1:], depth + 1),
        )

    def __get_adjusted_median__(self, objs, axis):
        """
        Adjusts median to be the FIRST occurrence of median axis value
        """
        assert len(objs) > 0
        assert axis in range(self.dimensions)
        # walk backwards from median
        median = len(objs) // 2
        i = median
        while i > 0:
            if objs[i].position()[axis] != objs[median].position()[axis]:
                return i + 1
            i -= 1
        return 0


class KdTreeScene(Scene):
    def __init__(self, num_objects=50, sim_time=10):
        super(KdTreeScene, self).__init__(num_objects)
        #Initialize fps & frames
        self.frame = 0
        self.fps_max = 0
        self.fps_min = 1000
        if sim_time is None:
            self.sim_time = 0
            self.SIM_TIME = 0
        else:
            self.sim_time = sim_time
            self.SIM_TIME = sim_time

        # set up objects in the scene
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
                mass=rand.randint(20, 40),
                start_p=position,
                start_v=Vector3(0, 0, rand.randint(20, 30))  # forward velocity
            )
            ball.update(1)  # force OM to update before turn_to_face
            ball.turn_to_face_p(origin)
            ball.rotate(5, Vector3(0, 1, 0))
            self.add_object_3d(ball)
        self.kd_tree = KdTree(self.objects_3d, dimensions=3)
        print "K-D Tree size: " + str(self.kd_tree.size())

    def update(self, delta):
        # update sim statistics
        self.sim_time -= delta
        self.frame += 1
        fps = 1 / delta
        if fps > self.fps_max and self.frame > 3:
            self.fps_max = fps
        if fps < self.fps_min:
            self.fps_min = fps

        # update scene
        self.kd_tree = KdTree(self.objects_3d, dimensions=3)
        self.check_for_collisions()
        super(KdTreeScene, self).update(delta)

        #If simulation is finished, print out info and exit
        if self.sim_time < 0 and self.SIM_TIME != 0:
            results_file = open("results.csv", "a")
            results_file.write(
                "%(name)s,%(a0)d,%(a1)d,%(a2)d,%(a3)f,%(a4)f,%(a5)d,%(a6)d\n" %
                {
                "name":("K-D Tree " + str(self.kd_tree.height()) + " Levels"),
                "a0": self.num_objects, "a1": self.SIM_TIME, "a2": self.frame,
                "a3": self.fps_min, "a4": self.fps_max, "a5": 0, "a6": 0
                }
            )
            results_file.close()
            exit()

    def draw(self):
        super(KdTreeScene, self).draw()

    def check_for_collisions(self):
        for o in self.objects_3d:
            subtree = self.kd_tree.get_subtree(o)
            if not subtree.left is None:
                self.__depth_first_collision_check__(
                    subtree=subtree.left,
                    test_obj=o
                )
            if not subtree.right is None:
                self.__depth_first_collision_check__(
                    subtree=subtree.right,
                    test_obj=o
                )

    def __depth_first_collision_check__(self, subtree, test_obj):
        """
        Test test_obj for collisions against objects in the subtree recursively

        :param subtree: the subtree of possible colliding objects
        :param test_obj: the object to test collision against
        """
        if subtree is None:
            return
        if test_obj.is_colliding(subtree.obj):
            test_obj.elastic_collide(subtree.obj)
        self.__depth_first_collision_check__(subtree.left, test_obj)
        self.__depth_first_collision_check__(subtree.right, test_obj)
