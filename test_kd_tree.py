from kd_tree_scene import *
import random as rand
import numpy as np

NUM_OBJECTS = 511

vectors = []
positions = []
for i in range(NUM_OBJECTS):
    vector = Vector3(
        rand.randint(-100, 100),
        rand.randint(-100, 100),
        rand.randint(-100, 100)
    )
    vectors.append(vector)
    positions.append([vector.x, vector.y, vector.z])

objs = []
for i in range(NUM_OBJECTS):
    ball = CollidableBall(colors.RED, mass=1, start_p=vectors[i])
    ball.update(0)
    objs.append(ball)

tree = KdTree(objs)

positions = sorted(positions)
print "POSITIONS:"
for p in positions:
    print p

print "\nMEDIAN:"
print str(np.median(positions, axis=0))

print "\nTREE:"
tree.print_tree()

print "\nLEFT CHILDREN:"
print str(tree.left_child_count())
