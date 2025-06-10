import math

import numpy as np

from Hitbox import Hitbox
from OBJ import OBJ


class Enemy(OBJ):
    def __init__(self, filename, move_speed=1, gravity=1, position=np.zeros(3), rotation=np.zeros(3),
                 scale=np.ones(3), floor=2.0, hitbox_size=np.array([3.4, 2, 3.4]),
                 hp=3, damage=0.5, swapyz=False):
        super().__init__(filename, position, rotation, scale, swapyz)
        self.gravity = gravity
        self.move_speed = move_speed
        self.floor = floor
        self.hitbox = Hitbox(position, hitbox_size)
        self.hp = hp
        self.damage = damage

    def move_to_target(self, target_pos, dt):
        direction_to_target = target_pos - self.position
        if np.any(direction_to_target):
            direction_to_target /= np.linalg.norm(direction_to_target)  # Normalize the vector
            self.position += direction_to_target * dt
            self.hitbox.position = self.position

    def rotate_to_target(self, target_pos):
        direction_to_target = target_pos - self.position
        if np.any(direction_to_target):
            direction_to_target /= np.linalg.norm(direction_to_target)
            angle = -math.atan2(direction_to_target[2],
                                direction_to_target[0])  # Berechnung des Winkels in der XZ-Ebene
            self.rotation[1] = math.degrees(angle)  # Setze die Y-Rotation des Feindes
        self.hitbox.position = self.position

    def apply_gravity(self, dt):
        if self.position[1] > self.floor:
            self.position[1] -= self.gravity * dt
        if self.position[1] < self.floor:
            self.position[1] = self.floor
        self.hitbox.position = self.position

    def kill_if_dead(self, enemies):
        if not self.hp:
            enemies.remove(self)
