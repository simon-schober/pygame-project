import sys

import numpy as np
import pygame
from OpenGL.GL import *
from pygame import *

from Hitbox import Hitbox


def clamp(x, minimum, maximum):
    return max(minimum, min(x, maximum))


class Player:
    def __init__(self, position=np.array([0.0, 10.0, 0.0]), rx=0, ry=0, move_speed=50, gravity=1,
                 direction=np.array([1.0, 0.0, 0.0]), up=np.array([0.0, 1.0, 0.0]),
                 hitbox_size=np.array([2.0, 4.0, 2.0]), hp=200.0, ammo=100,
                 velocity=np.array([0.0, 0.0, 0.0]), acceleration=np.array([0.0, 0.0, 0.0]), friction=1.0,
                 max_speed=500.0):
        self.velocity = velocity  # Geschwindigkeit des Spielers
        self.acceleration = acceleration  # Beschleunigung des Spielers
        self.friction = friction  # Reibung, um die Geschwindigkeit zu reduzieren
        self.max_speed = max_speed  # Maximale Geschwindigkeit
        # Restliche Initialisierung
        self.rx = rx
        self.ry = ry
        self.direction = direction
        self.position = position
        self.up = up
        self.right = np.cross(self.direction, self.up)
        self.right = self.right / np.linalg.norm(self.right)
        self.move_speed = move_speed
        self.gravity = gravity
        self.hitbox = Hitbox(position, hitbox_size)
        self.hp = hp
        self.ammo = ammo

    def compute_cam_direction(self, gun):
        # Convert yaw and pitch to radians
        yaw_rad = np.radians(self.rx)
        pitch_rad = np.radians(self.ry)

        # Compute direction vector based on yaw and pitch
        self.direction = np.array([
            np.cos(pitch_rad) * np.sin(yaw_rad),
            np.sin(pitch_rad),
            np.cos(pitch_rad) * np.cos(yaw_rad)
        ])
        self.direction = self.direction / np.linalg.norm(self.direction)

        # Compute right and up vectors
        self.right = np.cross(self.direction, self.up)
        self.right = self.right / np.linalg.norm(self.right)

        # Set gun rotation: apply yaw and pitch
        gun.rotation = [np.degrees(pitch_rad), np.degrees(yaw_rad), 0]

        # Position gun relative to player
        gun.position = self.position + np.array([-1.25, -0.5, 2.0])

        # Render the gun
        gun.render()

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

        # Bewegung
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

    def handle_events(self, enemies):
        # Event handling
        for e in pygame.event.get():
            if e.type == QUIT:
                sys.exit()
            elif e.type == KEYDOWN and e.key == K_ESCAPE:
                sys.exit()
            elif e.type == MOUSEMOTION:
                self.dx, self.dy = e.rel
                self.rx -= self.dx
                self.ry = clamp(self.ry - self.dy, -90, 90)
            elif e.type == MOUSEBUTTONDOWN and e.button == 1 and self.ammo > 0:  # Linke Maustaste
                self.raycast_shoot(enemies)

    def handle_movement(self, dt):
        keys = pygame.key.get_pressed()

        move = np.array([0.0, 0.0, 0.0])
        if keys[K_w]:
            move -= self.direction
        if keys[K_s]:
            move += self.direction
        if keys[K_a]:
            move += self.right
        if keys[K_d]:
            move -= self.right
        if np.linalg.norm(move) > 0:
            move = move / np.linalg.norm(move)
        self.acceleration = move * self.move_speed

        self.velocity += self.acceleration * dt
        self.velocity *= self.friction
        velocity_norm = np.linalg.norm(self.velocity)
        if velocity_norm > self.max_speed:
            self.velocity = self.velocity / velocity_norm * self.max_speed
        self.position[0] += self.velocity[0] * dt
        self.position[2] += self.velocity[2] * dt
        # self.position[1] bleibt unverändert

    def apply_gravity(self, objects, dt):
        if np.any([self.hitbox.check_collision(_object.hitbox) for _object in objects]):
            self.position[1] += dt
        else:
            self.position[1] -= self.gravity * dt

    def check_collision(self, enemies, dt, pushback_multiplier=18):
        for enemy in enemies:
            collision_vector = self.hitbox.get_collision_vector(enemy.hitbox)
            if collision_vector is not None:
                self.position -= collision_vector * pushback_multiplier * dt  # Spieler wird im Kollisionsvektor zurückgeschoben
                self.hp -= enemy.damage
                return True
        return False

    def update_positions(self, gun):
        self.hitbox.position = self.position
        gun.position = [self.position[0], self.position[1] - 1.25, self.position[2]]

    def raycast_shoot(self, enemies):
        ray_origin = self.position
        self.ammo -= 1
        for enemy in enemies:
            if enemy.hitbox.check_ray_collision(ray_origin, -self.direction):
                enemy.hp -= 1

                return True
        return False

    def kill_if_dead(self):
        if not self.hp:
            sys.exit()
