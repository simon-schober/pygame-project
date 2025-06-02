import sys

from pygame import *

from Enemy import *
from OBJ import *
from Object import Object
from Player import Player
from graphics import init_graphics

# Movement parameters
enemy_gravity = 1.0
enemy_move_speed = 1.0

player_gravity = 1.0
move_speed = 1.0
pan_speed = 1.0
init_graphics()

# LOAD OBJECT AFTER PYGAME INIT
enemies = [Enemy("assets/Cube.obj", [0.0, 10.0, 10.0], enemy_move_speed, enemy_gravity),
           Enemy("assets/Sphere.obj", [0.0, 10.0, 10.0], enemy_move_speed, enemy_gravity)]

objects = [Object("assets/Plane.obj", [0.0, 0.0, 10.0])]

cam_pos = np.array([0.0, 10.0, 0.0])
rx, ry = 0.0, 0.0
player = Player(cam_pos, rx, ry, move_speed, player_gravity)

# Generating all the objects
for enemy in enemies:
    enemy.generate()

for _object in objects:
    _object.generate()

# Initiating game clock
clock = pygame.time.Clock()

# Switching to editing the model view matrix
glMatrixMode(GL_MODELVIEW)

# Initialize camera position and orientation

# rotate = False


while True:
    dt = clock.tick(60) / 1000.0  # Delta time in seconds

    # Event handling
    for e in pygame.event.get():
        if e.type == QUIT:
            sys.exit()
        elif e.type == KEYDOWN and e.key == K_ESCAPE:
            sys.exit()
        elif e.type == MOUSEMOTION:
            player.dx, player.dy = e.rel
            player.rx -= player.dx
            player.ry -= player.dy

    # Handle keyboard input for movement

    player.compute_cam_direction()
    player.handle_keyboard_input(dt)
    player.apply_transformations()

    # Render objects
    for enemy in enemies:
        enemy.move_to_target(player.cam_pos, dt)
        enemy.render()

    for _object in objects:
        _object.render()

    pygame.display.flip()
