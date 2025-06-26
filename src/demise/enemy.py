import math

import numpy as np

from hitbox import Hitbox
from obj import OBJ


class Enemy(OBJ):
    def __init__(self, filename, move_speed=10, gravity=1, position=np.zeros(3), rotation=np.zeros(3),
                 scale=np.ones(3), hitbox_size=np.array([3.0, 3.0, 3.0]),
                 hp=3, damage=1.0, swapyz=False):
        super().__init__(filename, position, rotation, scale, hitbox_size, swapyz)
        self.gravity = gravity
        self.move_speed = move_speed
        self.hp = hp
        self.damage = damage

    def move_to_target(self, player, hitboxes_map, dt):
        direction_to_target = player.position - self.position
        if np.any(direction_to_target):
            direction_to_target /= np.linalg.norm(direction_to_target)
            new_position = self.position + direction_to_target * dt * self.move_speed
            temp_hitbox = Hitbox(new_position, self.hitbox.size)
            collision = False
            # Prüfe Kollision mit Spieler
            if temp_hitbox.check_collision(player.hitbox, player):
                collision = True
                if not player.healhack:
                    player.hp -= self.damage
            # Prüfe Kollisionen mit hitboxes_map
            if not collision:
                for map_hitbox in hitboxes_map:
                    if temp_hitbox.check_collision(map_hitbox, player):
                        collision = True
                        break
            if not collision:
                self.position = new_position

    def rotate_to_target(self, target_pos):
        direction_to_target = target_pos - self.position
        if np.any(direction_to_target):
            direction_to_target /= np.linalg.norm(direction_to_target)
            angle = -math.atan2(direction_to_target[2],
                                direction_to_target[0])
            self.rotation[1] = math.degrees(angle)

    def apply_gravity(self, objects, dt, player):
        if not player.flyhack:
            if not np.any(self.position > (0, 0, 0)):
                if np.any([self.hitbox.check_collision(
                        _object if isinstance(_object, Hitbox) else getattr(_object, "hitbox", None), player) for
                    _object in objects if isinstance(_object, Hitbox) or hasattr(_object, "hitbox")]):
                    self.position[1] += dt
                else:
                    try:
                        self.position[1] -= self.gravity * dt
                    except:
                        print("Fuck")

    def kill_if_dead(self, enemies):
        if not self.hp:
            enemies.remove(self)
            return True
        return False

    def update_positions(self):
        self.hitbox.position = self.position
