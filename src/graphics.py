from OpenGL.GL import *
from OpenGL.GLU import *


def init_graphics(viewport):
    # Set up OpenGL settings
    glViewport(0, 0, viewport[0], viewport[1])
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90.0, viewport[0] / float(viewport[1]), 1, 100000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Enable OpenGL features
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glShadeModel(GL_SMOOTH)

    # Himmellicht (Sonnenlicht) über der Map positionieren
    glEnable(GL_LIGHT1)
    sky_light_position = [0.0, 1000.0, 0.0, 0.0]  # Richtung von oben (w=0 für Richtungslicht)
    sky_light_diffuse = [1.0, 1.0, 0.95, 1.0]  # Warmes Sonnenlicht
    sky_light_ambient = [0.3, 0.3, 0.3, 1.0]  # Schwaches Umgebungslicht
    glLightfv(GL_LIGHT1, GL_POSITION, sky_light_position)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, sky_light_diffuse)
    glLightfv(GL_LIGHT1, GL_AMBIENT, sky_light_ambient)
