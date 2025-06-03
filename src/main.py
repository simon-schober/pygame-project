import sys

from pygame import *

from Enemy import *
from OBJ import *
from Object import Object
from Player import Player
from graphics import init_graphics
from start_menu import make_start_menu
#generally variables
Game_name = "Demise"
option_lines = ["Optins:", "", "Bewegen: ", "W          -->     Move vorward", "A          -->     Move Left", "S          -->     Move Backwards", "D          -->     Move Right", "Move Mous  -->     Rotate your Cracter", "Left Klick -->     Shoot with Gun" "", "You can`t change the Keybinds", "", "Press Arrow-Down-Key To go back to the menu" ]
credits_lines = ["Credits:", "", "Programmierung: ", "   Alexander Sief & Simon Schober", "Grafik: ", "   Vladimir Kandalintsev", "Sound: ", "   Simon Schober", "", "♥ Thx for playing our Game ♥", "", "Press Arrow-Down-Key To go back to the menu"]

# Movement parameterscredits_lines
enemy_gravity = 1.0
enemy_move_speed = 1.0

player_gravity = 1.0
move_speed = 1.0
pan_speed = 1.0

make_start_menu(Game_name, option_lines, credits_lines)

init_graphics()
pygame.mouse.set_visible(False)
# LOAD OBJECT AFTER PYGAME INIT
enemies = [Enemy("assets/Enemy.obj", [0.0, 10.0, 10.0], enemy_move_speed, enemy_gravity)]

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
