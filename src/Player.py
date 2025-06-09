import sys

import numpy as np
import pygame
from OpenGL.raw.GL.VERSION.GL_1_0 import glRotatef, glTranslatef, glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, \
    glLoadIdentity
from pygame import *


class Player:
    def __init__(self, cam_pos=np.array([0.0, 10.0, 0.0]), rx=0, ry=0, move_speed=10, gravity=1, floor=2.0,
                 direction=np.array([1.0, 0.0, 0.0]), up=np.array([0.0, 1.0, 0.0])):
        self.dx = 0
        self.dy = 0
        self.rx = rx
        self.ry = ry
        self.direction = [1.0, 0.0, 0.0]
        self.position = cam_pos
        self.direction = direction
        self.up = up
        self.right = np.cross(self.direction, self.up)
        self.right = self.right / np.linalg.norm(self.right)
        self.move_speed = move_speed
        self.gravity = gravity
        self.floor = floor

    def apply_cam_transforms(self):
        # Apply camera transformations
        glRotatef(-self.ry, 1, 0, 0)
        glRotatef(-self.rx, 0, 1, 0)
        glTranslatef(-self.position[0], -self.position[1], -self.position[2])

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
        self.right = np.cross(self.direction, self.up)
        self.right = self.right / np.linalg.norm(self.right)

    def apply_transformations(self):
        # Clear buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Apply camera transformations
        glRotatef(-self.ry, 1, 0, 0)
        glRotatef(-self.rx, 0, 1, 0)
        glTranslatef(-self.position[0], -self.position[1], -self.position[2])

    def handle_flying_movement(self, dt):
        keys = pygame.key.get_pressed()

        # Movement
        if keys[K_s]:
            self.position += self.direction * self.move_speed * dt
        if keys[K_w]:
            self.position -= self.direction * self.move_speed * dt
        if keys[K_d]:
            self.position -= self.right * self.move_speed * dt
        if keys[K_a]:
            self.position += self.right * self.move_speed * dt
        if keys[K_SPACE]:
            self.position += self.up * self.move_speed * dt
        if keys[K_LSHIFT]:
            self.position -= self.up * self.move_speed * dt

    def handle_events(self):
        # Event handling
        for e in pygame.event.get():
            if e.type == QUIT:
                sys.exit()
            elif e.type == KEYDOWN and e.key == K_ESCAPE:
                sys.exit()
            elif e.type == MOUSEMOTION:
                self.dx, self.dy = e.rel
                self.rx -= self.dx
                self.ry -= self.dy

    def handle_walking_movement(self, dt):
        keys = pygame.key.get_pressed()

        # Bewegung nur auf der XZ-Ebene (Y bleibt Höhe)
        move_dir = np.array([self.direction[0], 0, self.direction[2]])
        move_dir = move_dir / np.linalg.norm(move_dir)
        right_dir = np.array([self.right[0], 0, self.right[2]])
        right_dir = right_dir / np.linalg.norm(right_dir)

        if keys[K_s]:
            self.position += move_dir * self.move_speed * dt
        if keys[K_w]:
            self.position -= move_dir * self.move_speed * dt
        if keys[K_d]:
            self.position -= right_dir * self.move_speed * dt
        if keys[K_a]:
            self.position += right_dir * self.move_speed * dt

    def apply_gravity(self, dt):
        if self.position[1] > self.floor:
            self.position[1] -= self.gravity * dt