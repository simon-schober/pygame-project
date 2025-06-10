from Enemy import *
from OBJ import *
from Player import Player, render_crosshair
from graphics import init_graphics
from start_menu import make_start_menu

# Menu variables
Game_name = "Demise"
option_lines = [
    "Options:", "Move: ", "W          -->     Move forward", "",
    "A          -->     Move Left", "", "S          -->     Move Backwards", "",
    "D          -->     Move Right", "", "Move Mouse  -->     Rotate your Character", "",
    "Left click -->     Shoot with Gun", "",
    "You can`t change the Keybinds", "",
    "Tip: You can allways press ESC-Key ", "to leave the game (The score doesn't get saved)", "",
    "Press ESC-Key to go back to the menu"
]
credit_lines = [
    "Credits:", "", "Programming: ", "   Alexander Sief & Simon Schober", "",
    "Graphics: ", "   Vladimir Kandalintsev", "", "Sound: ", "   Simon Schober",
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

spawn_interval = 500  # Time in milliseconds
last_spawn_time = pygame.time.get_ticks()  # Point in time of last spawn

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
            player = Player(position=np.array([0.0, 0.0, 10.0]))

            # Generate all objects
            for enemy in enemies:
                enemy.generate()
            for _object in objects:
                _object.generate()

            pygame.mouse.set_visible(False)

        # Handle OpenGL rendering
        dt = clock.tick(60) / 1000.0  # Delta time in seconds

        player.handle_events(enemies)

        # Handle keyboard input for movement
        player.compute_cam_direction()
        player.handle_walking_movement(dt)
        player.apply_transformations()
        player.apply_gravity(dt)
        player.kill_if_dead()

        # Render objects
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        player.check_collision(enemies, dt)

        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time >= spawn_interval:
            enemy = Enemy("assets/Enemy.obj", position=(np.random.random(3) * 200) - 100)
            enemy.generate()
            enemies.append(enemy)
            last_spawn_time = current_time

        for enemy in enemies:
            enemy.move_to_target(player.position, dt)
            enemy.rotate_to_target(player.position)
            enemy.apply_gravity(dt)
            enemy.kill_if_dead(enemies)
            enemy.render()

        for _object in objects:
            _object.render()

        render_crosshair(screen_height, screen_width)

        pygame.display.flip()
