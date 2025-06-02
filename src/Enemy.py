import numpy as np

from Object import Object


class Enemy(Object):
    def __init__(self, filename, position, move_speed, gravity, swapyz=False):
        super().__init__(filename, position, swapyz)
        self.gravity = gravity
        self.move_speed = move_speed

    def move_to_target(self, target_pos, dt):
        direction_to_camera = target_pos - self.position
        direction_to_camera /= np.linalg.norm(direction_to_camera)  # Normalize the vector
        self.position += direction_to_camera * dt
