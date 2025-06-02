#!/usr/bin/env python
# Basic OBJ file viewer. needs objloader from:
#  http://www.pygame.org/wiki/OBJFileLoader
# LMB + move: rotate
# RMB + move: pan
# Scroll wheel: zoom in/out
import sys, pygame
from pygame.locals import *
from pygame.constants import *
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

positions = []
positions.append(())

# Generating all the objects
for obj in objects:
    obj.generate()

# Initiating game clock
clock = pygame.time.Clock()

# Switching to editing the model view matrix, which edits the relative position of models to the camera
glMatrixMode(GL_MODELVIEW)

# Initialize camera position and orientation
cam_pos = np.array([0.0, 0.0, 5.0])
rx, ry = 0.0, 0.0
rotate = move = False

while True:
    # Event handling
    for e in pygame.event.get():
        if e.type == QUIT:
            sys.exit()
        elif e.type == KEYDOWN and e.key == K_ESCAPE:
            sys.exit()
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                rotate = True
            elif e.button == 3:
                move = True
        elif e.type == MOUSEBUTTONUP:
            if e.button == 1:
                rotate = False
            elif e.button == 3:
                move = False
        elif e.type == MOUSEMOTION:
            dx, dy = e.rel
            if rotate:
                rx += dx
                ry += dy
            if move:
                # Convert angles to radians
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
                up = np.cross(right, direction)
                up = up / np.linalg.norm(up)

                # Adjust camera position
                pan_speed = 0.05
                cam_pos += -right * dx * pan_speed
                cam_pos += up * dy * pan_speed

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
    clock.tick(60)
