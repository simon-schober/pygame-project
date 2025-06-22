import math

import numpy as np

from OBJ import OBJ
from Hitbox import Hitbox


class Enemy(OBJ):
    def __init__(self, filename, move_speed=1, gravity=1, position=np.zeros(3), rotation=np.zeros(3),
                 scale=np.ones(3), hitbox_size=np.array([3.0, 3.0, 3.0]),
                 hp=3, damage=1.0, swapyz=False):
        super().__init__(filename, position, rotation, scale, hitbox_size, swapyz)
        self.gravity = gravity
        self.move_speed = move_speed
        self.hp = hp
        self.damage = damage

    def move_to_target(self, target_pos, dt):
        direction_to_target = target_pos - self.position
        if np.any(direction_to_target):
            direction_to_target /= np.linalg.norm(direction_to_target)
            self.position += direction_to_target * dt

    def rotate_to_target(self, target_pos):
        direction_to_target = target_pos - self.position
        if np.any(direction_to_target):
            direction_to_target /= np.linalg.norm(direction_to_target)
            angle = -math.atan2(direction_to_target[2],
                                direction_to_target[0])
            self.rotation[1] = math.degrees(angle)

    def apply_gravity(self, objects, dt, player):
        if not player.flyhack:
            if not any(self.position > (0,0,0)):
                if np.any([self.hitbox.check_collision(_object if isinstance(_object, Hitbox) else getattr(_object, "hitbox", None),player)for _object in objects if isinstance(_object, Hitbox) or hasattr(_object, "hitbox")]):
                    self.position[1] += dt
                else:
                    self.position[1] -= self.gravity * dt

    def kill_if_dead(self, enemies, player):
        if not self.hp:
            enemies.remove(self)

    def update_positions(self):
        self.hitbox.position = self.position
