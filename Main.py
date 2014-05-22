from pyglet.gl import *

__author__ = 'James'

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys

from Colors import *
from Scene import Scene


# CONSTANTS
VIEWPORT_WIDTH = 1280
VIEWPORT_HEIGHT = 720
WINDOW_X = 300
WINDOW_Y = 200
WINDOW_NAME = "Collision Simulation"

# GLOBAL VARS
scene = Scene()


def usage():
    print "python " + str(sys.argv[0])


def resize():
    glViewport(0, 0, VIEWPORT_WIDTH, VIEWPORT_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, VIEWPORT_WIDTH / float(VIEWPORT_HEIGHT), 1.0, 10000)

def draw():
    set_lighting()


    # draw_axes(1000)
    #
    # glPushMatrix()
    # glLoadIdentity()
    # gluLookAt(
    #     1000, 1000, 2000,     # eye
    #     0, 0, 0,        # look-at
    #     0, 1, 0         # up
    # )
    # glColor4fv(WHITE)
    # glutWireCube(1000)
    # glColor4fv(RED)
    # glutSolidSphere(50, 30, 20)
    # glPopMatrix()

    scene.update()
    scene.draw()

    glutSwapBuffers()


# def draw_axes(length):
#     glMatrixMode(GL_MODELVIEW)
#
#     glPushMatrix()
#
#     glLineWidth(1)
#     glBegin(GL_LINES)
#     glColor4fv(RED)
#     glVertex3f(0, 0, 0)
#     glVertex3f(length, 0, 0)
#
#     glColor4fv(GREEN)
#     glVertex3f(0,0,0)
#     glVertex3f(0,length,0)
#
#     glColor4fv(BLUE)
#     glVertex3f(0, 0, 0)
#     glVertex3f(0, 0, length)
#     glEnd()
#     glLineWidth(1)
#
#     glPopMatrix()


def set_lighting():
    glClearColor(0.5, 0.7, 0.9, 1.0)  # sky bg
    # glClearColor(0.0, 0.0, 0.0, 1.0)  # black bg
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)

    # set light 0 as diffuse directional light
    glLightfv(GL_LIGHT0, GL_POSITION, [1000.0, 1000.0, 500.0, 0.0])  # position
    glLightfv(GL_LIGHT0, GL_DIFFUSE, OFF_WHITE)  # color
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    # glLightfv(GL_LIGHT0, GL_SPECULAR, WHITE)  # color
    # glMaterialfv(GL_FRONT, GL_SPECULAR, WHITE)
    # glMateriali(GL_FRONT, GL_SHININESS, 60)
    glEnable(GL_LIGHT0)

    # add ambient lighting
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, DARK_GRAY)


def main():
    glutInit(sys.argv)

    # init sim window
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(VIEWPORT_WIDTH, VIEWPORT_HEIGHT)
    glutInitWindowPosition(WINDOW_X, WINDOW_Y)

    # create sim window
    sim_window = glutCreateWindow(WINDOW_NAME)
    glutDisplayFunc(draw)
    glutReshapeFunc(resize)

    # glMatrixMode(GL_PROJECTION)
    # gluPerspective(45.0, float(VIEWPORT_WIDTH) / VIEWPORT_HEIGHT, 1.0, 10000)
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(
        1000, 1000, 2000,     # eye
        0, 0, 0,        # look-at
        0, 1, 0         # up
    )
    glPushMatrix()

    glutMainLoop()


if __name__ == "__main__":
    main()
