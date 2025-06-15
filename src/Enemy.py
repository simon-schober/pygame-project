import math

import numpy as np

from OBJ import OBJ


class Enemy(OBJ):
    def __init__(self, filename, move_speed=1, gravity=1, position=np.zeros(3), rotation=np.zeros(3),
                 scale=np.ones(3), hitbox_size=np.array([3.4, 3.0, 3.4]),
                 hp=3, damage=1.0, swapyz=False):
        super().__init__(filename, position, rotation, scale, hitbox_size, swapyz)
        self.gravity = gravity
        self.move_speed = move_speed
        self.hp = hp
        self.damage = damage

    def move_to_target(self, target_pos, dt):
        direction_to_target = target_pos - self.position
        if np.any(direction_to_target):
            direction_to_target /= np.linalg.norm(direction_to_target)  # Normalize the vector
            self.position += direction_to_target * dt

    def rotate_to_target(self, target_pos):
        direction_to_target = target_pos - self.position
        if np.any(direction_to_target):
            direction_to_target /= np.linalg.norm(direction_to_target)
            angle = -math.atan2(direction_to_target[2],
                                direction_to_target[0])  # Berechnung des Winkels in der XZ-Ebene
            self.rotation[1] = math.degrees(angle)  # Setze die Y-Rotation des Feindes

    def apply_gravity(self, objects, dt, player):
        if not player.flyhack:
            if np.any([self.hitbox.check_collision(_object.hitbox, player) for _object in objects]):
                self.position[1] += dt
            else:
                self.position[1] -= self.gravity * dt

    def kill_if_dead(self, enemies, player):
        if not self.hp:
            enemies.remove(self)

    def update_positions(self):
        self.hitbox.position = self.position