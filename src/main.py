from Enemy import *
from OBJ import *
from Player import Player
from graphics import init_graphics
from start_menu import make_start_menu

# Menu variables
Game_name = "Demise"
option_lines = [
    "Options:", "Bewegen: ", "W          -->     Move vorward", "",
    "A          -->     Move Left", "", "S          -->     Move Backwards", "",
    "D          -->     Move Right", "", "Move Mous  -->     Rotate your Cracter", "",
    "Left Klick -->     Shoot with Gun", "",
    "You can`t change the Keybinds", "",
    "Tipp: You can allways press ESC-Key ", "to leave the game (The score doesn`t get saved)", "",
    "Press ESC-Key to go back to the menu"
]
credit_lines = [
    "Credits:", "", "Programmierung: ", "   Alexander Sief & Simon Schober", "",
    "Grafik: ", "   Vladimir Kandalintsev", "", "Sound: ", "   Simon Schober",
    "", "", "♥ Thx for playing our Game ♥", "",
    "Press ESC-Key to go back to the menu"
]
start_menu_scale = 1.03
current_state_menu = "main"  # main, options, credits

# State management
current_state = "menu"

# Initialize Pygame
pygame.init()
pygame.font.init()

# Initialize screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF)
pygame.display.set_caption(Game_name)
screen_width, screen_height = screen.get_size()

# Game clock
clock = pygame.time.Clock()

# Initialize OpenGL settings (only once)
opengl_initialized = False

player, enemies, objects = None, None, None

# Main loop
while True:
    if current_state == "menu":
        # Render the start menu
        current_state = make_start_menu(screen, Game_name, option_lines, credit_lines, start_menu_scale,
                                        current_state_menu)
    elif current_state == "game":
        if not opengl_initialized:
            # Initialize OpenGL context and settings
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.OPENGL | pygame.DOUBLEBUF)
            init_graphics((screen.get_width(), screen.get_height()))
            opengl_initialized = True

            # Initialize game objects
            enemies = [Enemy("assets/Enemy.obj")]
            objects = [OBJ("assets/Plane.obj")]
            player = Player()

            # Generate all objects
            for enemy in enemies:
                enemy.generate()
            for _object in objects:
                _object.generate()

            pygame.mouse.set_visible(False)

        # Handle OpenGL rendering
        dt = clock.tick(60) / 1000.0  # Delta time in seconds

        player.handle_events()

        # Handle keyboard input for movement
        player.compute_cam_direction()
        player.handle_walking_movement(dt)
        player.apply_transformations()

        # Render objects
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for enemy in enemies:
            enemy.move_to_target(player.position, dt)
            enemy.rotate_to_target(player.position)
            enemy.apply_gravity(dt)
            enemy.render()

        for _object in objects:
            _object.render()

        player.apply_gravity(dt)

        pygame.display.flip()
