import sys
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# IMPORT OBJECT LOADER
from objloader import *
from util import init_graphics

init_graphics()

# LOAD OBJECT AFTER PYGAME INIT
objects = []
objects.append(OBJ("assets/Cube.obj", swapyz=True))
objects.append(OBJ("assets/Sphere.obj", swapyz=True))

# Generating all the objects
for obj in objects:
    obj.generate()

# Initiating game clock
clock = pygame.time.Clock()

# Switching to editing the model view matrix
glMatrixMode(GL_MODELVIEW)

# Initialize camera position and orientation
cam_pos = np.array([0.0, 0.0, 5.0])
rx, ry = 0.0, 0.0
rotate = False

# Movement parameters
move_speed = 0.1

while True:
    dt = clock.tick(60) / 1000.0  # Delta time in seconds

    # Event handling
    for e in pygame.event.get():
        if e.type == QUIT:
            sys.exit()
        elif e.type == KEYDOWN and e.key == K_ESCAPE:
            sys.exit()
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                rotate = True
        elif e.type == MOUSEBUTTONUP:
            if e.button == 1:
                rotate = False
        elif e.type == MOUSEMOTION:
            dx, dy = e.rel
            if rotate:
                rx -= dx
                ry -= dy

    # Handle keyboard input for movement
    keys = pygame.key.get_pressed()
    yaw_rad = np.radians(rx)
    pitch_rad = np.radians(ry)

    # Compute direction vector
    direction = np.array([
        np.cos(pitch_rad) * np.sin(yaw_rad),
        np.sin(pitch_rad),
        np.cos(pitch_rad) * np.cos(yaw_rad)
    ])
    direction = direction / np.linalg.norm(direction)

    # Compute right and up vectors
    up = np.array([0.0, 1.0, 0.0])
    right = np.cross(direction, up)
    right = right / np.linalg.norm(right)

    # Movement
    if keys[K_s]:
        cam_pos += direction * move_speed
    if keys[K_w]:
        cam_pos -= direction * move_speed
    if keys[K_d]:
        cam_pos -= right * move_speed
    if keys[K_a]:
        cam_pos += right * move_speed
    if keys[K_SPACE]:
        cam_pos += up * move_speed
    if keys[K_LSHIFT]:
        cam_pos -= up * move_speed

    # Clear buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Apply camera transformations
    glRotatef(-ry, 1, 0, 0)
    glRotatef(-rx, 0, 1, 0)
    glTranslatef(-cam_pos[0], -cam_pos[1], -cam_pos[2])

    # Render objects
    for obj in objects:
        obj.render()

    pygame.display.flip()

