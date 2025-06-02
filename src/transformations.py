import numpy as np
from OpenGL.raw.GL.VERSION.GL_1_0 import glRotatef, glTranslatef, glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, \
    glLoadIdentity


def apply_cam_transforms(rx, ry, cam_pos):
    # Apply camera transformations
    glRotatef(-ry, 1, 0, 0)
    glRotatef(-rx, 0, 1, 0)
    glTranslatef(-cam_pos[0], -cam_pos[1], -cam_pos[2])


def compute_cam_direction(rx, ry):
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
    return direction, right, up


def apply_transformations(cam_pos, dt, rx, ry):
    # Clear buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    # Apply camera transformations
    glRotatef(-ry * dt, 1, 0, 0)
    glRotatef(-rx * dt, 0, 1, 0)
    glTranslatef(-cam_pos[0] * dt, -cam_pos[1] * dt, -cam_pos[2] * dt)
