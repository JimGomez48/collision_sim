# Pass a single integer argument (1, 2 or 3) to indicate the scene and collision detection algorithm to be employed -
# 1 - Top down octree
# 2 - Bottom up octree
# 3 - Sweep and prune

from pyglet import clock
from pyglet.gl import *
from OpenGL.GLUT import *
import argparse

from octtree_bottomup_scene import OctTreeBottomUpScene
from octtree_topdown_scene import OctTreeTopDownScene
from sweep_and_prune_scene import SAPScene
from brute_force_scene import BruteForceScene
from no_collisions_scene import NoCollisionsScene
from octtree_alternate import OctTreeAltScene

VIEWPORT_WIDTH = 1280
VIEWPORT_HEIGHT = 800
WINDOW_X = 300
WINDOW_Y = 200
WINDOW_NAME = "Collision Simulation: "

parser = argparse.ArgumentParser(
    description="This simulation demonstrates the use of different collision "
                "detection techniques for efficiently animating many objects "
                "in a scene"
)
parser.add_argument("scene_id", type=int,
                    choices=range(1, 7),
                    help="1. Top-down Octree 2. K-d Tree 3. Sweep-and-Prune "
                         "4. Brute-Force 5. No Collision 6. Octree Alternate")
args = parser.parse_args()
if (args.scene_id == 1):
    scene = OctTreeTopDownScene()
    WINDOW_NAME += "Octree Top-Down"
elif (args.scene_id == 2):
    scene = OctTreeBottomUpScene()
    WINDOW_NAME += "Octree Bottom-Up"
elif (args.scene_id == 3):
    scene = SAPScene()
    WINDOW_NAME += "Sweep-and-Prune"
elif (args.scene_id == 4):
    scene = BruteForceScene()
    WINDOW_NAME += "Brute-Force"
elif (args.scene_id == 5):
    scene = NoCollisionsScene()
    WINDOW_NAME += "No Collisions"
elif (args.scene_id == 6):
    scene = OctTreeAltScene()
    WINDOW_NAME += "Octree Alternate"

# GLOBAL VARS
window = pyglet.window.Window(VIEWPORT_WIDTH, VIEWPORT_HEIGHT)
window.set_location(WINDOW_X, WINDOW_Y)
window.set_caption(WINDOW_NAME)

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
