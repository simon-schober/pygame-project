from enemy import *
from graphics import init_graphics
from input import handle_input
from objloader import *

init_graphics()

# LOAD OBJECT AFTER PYGAME INIT
enemies = [Enemy("assets/Cube.obj", [0.0, 0.0, 0.0], swapyz=True),
           Enemy("assets/Sphere.obj", [0.0, 10.0, 0.0], swapyz=True)]

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
move_speed = 1
pan_speed = 1

while True:
    dt = clock.tick(60) / 1000.0  # Delta time in seconds

    # Event handling
    rx, ry = handle_input(cam_pos, rx, ry, move_speed, dt, pan_speed)

    # Render objects
    for enemy in enemies:
        enemy.move_to_target(cam_pos, dt)
        enemy.render()

    pygame.display.flip()
