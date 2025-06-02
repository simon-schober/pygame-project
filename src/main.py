import sys
from pygame.locals import *
from enemy import *

# IMPORT OBJECT LOADER
from objloader import *
from src.transformations import apply_cam_transforms
from graphics import init_graphics

init_graphics()

# LOAD OBJECT AFTER PYGAME INIT
enemies = [Enemy("assets/Cube.obj", [0.0, 0.0, 0.0], swapyz=True), Enemy("assets/Sphere.obj", [0.0, 10.0, 0.0], swapyz=True)]

# Generating all the objects
for enemy in enemies:
    enemy.generate()

# Initiating game clock
clock = pygame.time.Clock()

# Switching to editing the model view matrix
glMatrixMode(GL_MODELVIEW)

# Initialize camera position and orientation
cam_pos = np.array([0.0, 0.0, 5.0])
rx, ry = 0.0, 0.0
# rotate = False

# Movement parameters
move_speed = 0.1

while True:
    dt = clock.tick(60) / 1000.0  # Delta time in seconds

    # Event handling
    for e in pygame.event.get():
        if e.type == QUIT:
            sys.exit()
        elif e.type == KEYDOWN and e.key == K_ESCAPE:
            sys.exit()
        # elif e.type == MOUSEBUTTONDOWN:
        #     if e.button == 1:
        #         rotate = True
        # elif e.type == MOUSEBUTTONUP:
        #     if e.button == 1:
        #         rotate = False
        elif e.type == MOUSEMOTION:
            dx, dy = e.rel
            # if rotate:
            #     rx -= dx
            #     ry -= dy
            rx -= dx
            ry -= dy

    # Handle keyboard input for movement
    keys = pygame.key.get_pressed()
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

    # Movement
    if keys[K_s]:
        cam_pos += direction * move_speed
    if keys[K_w]:
        cam_pos -= direction * move_speed
    if keys[K_d]:
        cam_pos -= right * move_speed
    if keys[K_a]:
        cam_pos += right * move_speed
    if keys[K_SPACE]:
        cam_pos += up * move_speed
    if keys[K_LSHIFT]:
        cam_pos -= up * move_speed

    # Clear buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    apply_cam_transforms(rx, ry, cam_pos)

    # Render objects
    for enemy in enemies:
        enemy.move_to_target(cam_pos, dt)
        enemy.render()

    pygame.display.flip()

