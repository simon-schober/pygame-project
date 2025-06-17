from OpenGL.GL import *
from OpenGL.GLU import *


def init_graphics(viewport):
    # Set up OpenGL settings
    glViewport(0, 0, viewport[0], viewport[1])
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Render-Distanz-Limit entfernen ("far"-Wert sehr hoch setzen)
    gluPerspective(90.0, viewport[0] / float(viewport[1]), 1, 100000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Enable OpenGL features
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glShadeModel(GL_SMOOTH)
