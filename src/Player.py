import numpy as np
import pygame
from OpenGL.raw.GL.VERSION.GL_1_0 import glRotatef, glTranslatef, glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, \
    glLoadIdentity
from pygame import *


class Player:
    def __init__(self, cam_pos, rx, ry, move_speed, gravity):
        self.rx = rx
        self.ry = ry
        self.direction = [1.0, 0.0, 0.0]
        self.cam_pos = cam_pos
        self.up = np.array([0.0, 1.0, 0.0])
        self.right = np.cross(self.direction, self.up)
        self.right = self.right / np.linalg.norm(self.right)
        self.move_speed = move_speed
        self.gravity = gravity

    def apply_cam_transforms(self):
        # Apply camera transformations
        glRotatef(-self.ry, 1, 0, 0)
        glRotatef(-self.rx, 0, 1, 0)
        glTranslatef(-self.cam_pos[0], -self.cam_pos[1], -self.cam_pos[2])

    def compute_cam_direction(self):
        yaw_rad = np.radians(self.rx)
        pitch_rad = np.radians(self.ry)

        # Compute direction vector
        self.direction = np.array([
            np.cos(pitch_rad) * np.sin(yaw_rad),
            np.sin(pitch_rad),
            np.cos(pitch_rad) * np.cos(yaw_rad)
        ])
        self.direction = self.direction / np.linalg.norm(self.direction)

        # Compute right and up vectors
        self.up = np.array([0.0, 1.0, 0.0])
        self.right = np.cross(self.direction, self.up)
        self.right = self.right / np.linalg.norm(self.right)

    def apply_transformations(self):
        # Clear buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Apply camera transformations
        glRotatef(-self.ry, 1, 0, 0)
        glRotatef(-self.rx, 0, 1, 0)
        glTranslatef(-self.cam_pos[0], -self.cam_pos[1], -self.cam_pos[2])

    def handle_keyboard_input(self, dt):
        keys = pygame.key.get_pressed()

        # Movement
        if keys[K_s]:
            self.cam_pos += self.direction * self.move_speed * dt
        if keys[K_w]:
            self.cam_pos -= self.direction * self.move_speed * dt
        if keys[K_d]:
            self.cam_pos -= self.right * self.move_speed * dt
        if keys[K_a]:
            self.cam_pos += self.right * self.move_speed * dt
        if keys[K_SPACE]:
            self.cam_pos += self.up * self.move_speed * dt
        if keys[K_LSHIFT]:
            self.cam_pos -= self.up * self.move_speed * dt
