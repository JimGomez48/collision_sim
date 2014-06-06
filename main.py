from pyglet import clock
from pyglet.gl import *
from OpenGL.GLUT import *
import argparse

from no_collisions_scene import NoCollisionsScene
from brute_force_scene import BruteForceScene
from octree_scene import OctreeScene
from kd_tree_scene import KdTreeScene
from sweep_and_prune_scene import SAPScene

# Pass two command line integer arguments -
#
# 1. Scene -
# 1 - no collisions
# 2 - brute force
# 3 - octree
# 4 - k-d tree
# 5 - sweep and prune
#
# 2. Number of objects

VIEWPORT_WIDTH = 1280
VIEWPORT_HEIGHT = 800
WINDOW_X = 200
WINDOW_Y = 100
WINDOW_NAME = "Collision Simulation: "

parser = argparse.ArgumentParser(
    description="This simulation demonstrates the use of different collision "
                "detection techniques for efficiently animating many objects "
                "in a scene"
)
parser.add_argument(
    "scene_id",
    type=int,
    metavar="scene_id",
    choices=range(1, 7),
    help="{1} No Collision {2} Brute-Force {3} Octree {4} K-d Tree "
         "{5} Sweep-and-Prune"
)
parser.add_argument(
    "num_objects",
    type=int,
    help="The number of objects to render in the scene"
)

args = parser.parse_args()
title = ""
if args.scene_id == 1:
    scene = NoCollisionsScene(args.num_objects)
    title = "No Collisions"
elif args.scene_id == 2:
    scene = BruteForceScene(args.num_objects)
    title = "Brute-Force"
elif args.scene_id == 3:
    scene = OctreeScene(args.num_objects)
    title = "Octree"
elif args.scene_id == 4:
    scene = KdTreeScene(args.num_objects)
    title = "K-D Tree"
elif args.scene_id == 5:
    scene = SAPScene(args.num_objects)
    title = "Sweep-and-Prune"
else:
    parser.print_usage()
    raise ValueError("Invalid scene argument")
WINDOW_NAME += title

window = pyglet.window.Window(VIEWPORT_WIDTH, VIEWPORT_HEIGHT)
window.set_location(WINDOW_X, WINDOW_Y)
window.set_caption(WINDOW_NAME)
title_label = pyglet.text.Label(
    text=title,
    font_name='Arial',
    font_size=36,
    color=[255, 255, 255, 255],
    x=-600, y=330,
    anchor_x='left', anchor_y='bottom'
)
fps_label = pyglet.text.Label(
    'FPS: ',
    font_name='Arial',
    font_size=36,
    color=[0, 255, 0, 255],
    x=330, y=-360,
    anchor_x='left', anchor_y='bottom'
)
num_objs_label = pyglet.text.Label(
    text='# Objs: ' + str(scene.num_objects),
    font_name='Arial',
    font_size=36,
    color=[255, 0, 0, 255],
    x=-600, y=-360,
    anchor_x='left', anchor_y='bottom'
)


@window.event
def on_resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, width / float(height), 1.0, 10000)
    glMatrixMode(GL_MODELVIEW)


@window.event
def on_draw():
    window.clear()
    set_3d()
    scene.draw()
    set_2d()
    title_label.draw()
    num_objs_label.draw()
    fps_label.text = "FPS: " + str("%.2f" % clock.get_fps())
    fps_label.draw()
    unset_2d()


def update(delta):
    scene.update(float(delta))


def set_3d():
    # set up perspective view frustrum
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, VIEWPORT_WIDTH / float(VIEWPORT_HEIGHT), 1.0, 50000)
    # reset modelview matrix
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def set_2d():
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glDisable(GL_COLOR_MATERIAL)
    # store the projection matrix to restore later
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    # load orthographic projection matrix
    glLoadIdentity()
    far = 8192
    glOrtho(-VIEWPORT_WIDTH / 2., VIEWPORT_WIDTH / 2.,
            -VIEWPORT_HEIGHT / 2., VIEWPORT_HEIGHT / 2., 0, far)
    # reset modelview
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def unset_2d():
    # load back the projection matrix saved before
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()


if __name__ == "__main__":
    clock.schedule_interval(update, 1 / 60.0)  # update at 60 fps
    glutInit(sys.argv)
    pyglet.app.run()
