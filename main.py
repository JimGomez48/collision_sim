__author__ = 'James'

import pyglet
from pyglet import clock
from pyglet.gl import *
from OpenGL.GLUT import *

from scene import Scene
from octtree_bottomup_scene import OctTreeBottomUpScene
from octtree_topdown_scene import OctTreeTopDownScene


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

# scene = Scene()
scene = OctTreeTopDownScene()

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
    clock.schedule_interval(render, 1 / 30.0)  # render at 30 fps
    glutInit(sys.argv)
    pyglet.app.run()
