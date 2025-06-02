from objloader import OBJ
import numpy as np

class Enemy(OBJ):
    def __init__(self, filename, position, swapyz=False):
        super().__init__(filename, swapyz)
        self.position = position
    def move_to_target(self, target_pos, dt):
        direction_to_camera = target_pos - self.position
        direction_to_camera /= np.linalg.norm(direction_to_camera)  # Normalize the vector
        self.position += direction_to_camera * dt