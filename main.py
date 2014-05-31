# Pass a single integer argument (1, 2 or 3) to indicate the scene and collision detection algorithm to be employed -
# 1 - Top down octree
# 2 - Bottom up octree
# 3 - Sweep and prune

__author__ = 'James'

import pyglet
from pyglet import clock
from pyglet.gl import *
from OpenGL.GLUT import *

from octtree_bottomup_scene import OctTreeBottomUpScene
from octtree_topdown_scene import OctTreeTopDownScene
from sweep_and_prune_scene import SAPScene
from brute_force_scene import BruteForceScene
from no_collisions_scene import NoCollisionsScene

# CONSTANTS
VIEWPORT_WIDTH = 1280
VIEWPORT_HEIGHT = 800
WINDOW_X = 300
WINDOW_Y = 200
WINDOW_NAME = "Collision Simulation"

# GLOBAL VARS
window = pyglet.window.Window(VIEWPORT_WIDTH, VIEWPORT_HEIGHT)
window.set_location(WINDOW_X, WINDOW_Y)
window.set_caption(WINDOW_NAME)

if (len(sys.argv) != 2):
    raise ValueError("Argument missing. Please specify the scene and collision detection algorithm to be employed ")
elif (int(sys.argv[1]) == 1):
    scene = OctTreeTopDownScene()
elif (int(sys.argv[1]) == 2):
    scene = OctTreeBottomUpScene()
elif (int(sys.argv[1]) == 3):
    scene = SAPScene()
elif (int(sys.argv[1]) == 4):
    scene = BruteForceScene()
elif (int(sys.argv[1]) == 5):
    scene = NoCollisionsScene()

@window.event
def on_resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(gl.GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, width / float(height), 1.0, 10000)
    glMatrixMode(gl.GL_MODELVIEW)


def render(delta):
    window.clear()
    # update the scene
    scene.update(float(delta))

    # set up perspective view frustrum
    glMatrixMode(gl.GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, VIEWPORT_WIDTH / float(VIEWPORT_HEIGHT), 1.0, 10000)
    # draw the scene
    scene.draw()


if __name__ == "__main__":
    clock.schedule_interval(render, 1 / 60.0)  # render at 30 fps
    glutInit(sys.argv)
    pyglet.app.run()
