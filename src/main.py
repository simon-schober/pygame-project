from Enemy import *
from OBJ import *
from Player import *
from graphics import init_graphics
from start_menu import make_start_menu

# Menu variables
Game_name = "Demise"
option_lines = [
    "Options:", "Move: ", "W          -->     Move forward", "",
    "A          -->     Move Left", "", "S          -->     Move Backwards", "",
    "D          -->     Move Right", "", "Move Mouse  -->     Rotate your Character", "",
    "Left click -->     Shoot with Gun", "",
    "R          -->     Reload the gun ammo", ""
                                              "You can't change the Keybinds", "",
    "Press ESC-Key to go back to the menu"
]
credit_lines = [
    "Credits:", "", "Programming: ", "   Alexander Sief & Simon Schober", "",
    "Graphics: ", "   Vladimir Kandalintsev", "", "Sound: ", "   Simon Schober",
    "", "", "♥ Thx for playing our Game ♥", "",
    "Press ESC-Key to go back to the menu"
]
current_state_menu = "main"  # main, options, credits

# State management
current_state = "menu"

# Initialize Pygame and font
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Musik abspielen: DEMISE.wav im Hintergrund und in Dauerschleife
pygame.mixer.music.load('assets/Sounds/DEMISE.wav')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)  # -1 bedeutet Endlosschleife

# Initialize screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF)
pygame.display.set_caption(Game_name)
screen_width, screen_height = screen.get_size()
start_menu_scale = (1.03 / 900) * screen_height
# Game clock
clock = pygame.time.Clock()

# Initialize OpenGL settings (only once)
opengl_initialized = False

player, enemies, objects = None, None, None

spawn_interval = 2000  # Time in milliseconds
last_spawn_time = pygame.time.get_ticks()  # Point in time of last spawn
last_time = pygame.time.get_ticks()

heal_time = 5000  # How long it takes so the player generate a new life (milliseconds)
healing_number = 1  # How much does the player heal after the healtime ended
hp_max = 200  # how much Hp can the Player have
ammo_max = 100
max_enemies = 1000

# Create font for the HP bar
hp_font = pygame.font.Font("assets/StartMenu/Font/BLKCHCRY.TTF", 145)


def render_text_and_image(screen_width, screen_height):
    start_menu_scale = 1.003 / 900 * screen_height

    # Load and scale HP bar texture
    hp_bar_field = pygame.image.load('assets/Game/Hp_bar_texture.png').convert_alpha()
    hp_bar_field = pygame.transform.smoothscale(hp_bar_field, (int(screen_width * (start_menu_scale - 0.94)),
                                                               int(screen_width * (
                                                                       start_menu_scale - 0.94) * hp_bar_field.get_height() / hp_bar_field.get_width())))

    render_2D_texture(hp_bar_field, 10, 10, screen_width, screen_height)

    # HP bar logic
    hp_surface = pygame.Surface((320, 55), pygame.SRCALPHA)
    color = (
        (53, 211, 2) if player.hp > 155 else (254, 102, 5) if player.hp > 100 else (138, 5, 6) if player.hp > 45 else (
            70, 5, 5))
    pygame.draw.rect(hp_surface, color, (0, 0, 320 * (player.hp / hp_max), 55))
    render_2D_texture(hp_surface, 115
                      , 100, screen_width, screen_height)

    # Bullet image
    bullet_pic = pygame.image.load("assets/Game/ammo-rifle.png").convert_alpha()
    bullet_width = int(screen_width * 0.1)
    bullet_height = int(bullet_pic.get_height() * bullet_width / bullet_pic.get_width())
    bullet_pic = pygame.transform.smoothscale(bullet_pic, (bullet_width, bullet_height))
    render_2D_texture(bullet_pic, screen_width - 300, -10, screen_width, screen_height)

    crosshair = pygame.image.load('assets/Game/crosshair.png').convert_alpha()
    crosshair_size = int(screen_width * 0.02)
    crosshair = pygame.transform.smoothscale(crosshair, (crosshair_size, crosshair_size))
    render_2D_texture(crosshair, (screen_width - crosshair.get_width()) // 2,
                      (screen_height - crosshair.get_height()) // 2, screen_width, screen_height)

    # Fonts and Texts
    hp_font_size = int((175 // (screen_height * 0.00078125)) / 2)
    bullet_font_size = int((100 // (screen_height * 0.00078125)) / 2)

    hp_font = pygame.font.Font('assets/StartMenu/Font/BLKCHCRY.TTF', hp_font_size)
    bullet_font = pygame.font.Font('assets/StartMenu/Font/BLKCHCRY.TTF', bullet_font_size)

    # HP text
    text_surface = hp_font.render(f"{int(player.hp)}", True, (97, 93, 87))
    render_2D_texture(text_surface, 270, 140, screen_width, screen_height)

    # Ammo text
    ammo_surface = bullet_font.render(f"{player.ammo}/{ammo_max}", True, (97, 93, 87))
    render_2D_texture(ammo_surface, screen_width - 300, 140, screen_width, screen_height)

    # Magazine count
    mag_surface = bullet_font.render(f"{player.mag_ammo}/{int(player.mag_size)}", True, (200, 200, 200))
    render_2D_texture(mag_surface, screen_width - 300, 210, screen_width, screen_height)


# Main loop
pygame.mouse.set_visible(False)
while True:
    current_time = pygame.time.get_ticks()
    if current_state == "menu":
        current_state = make_start_menu(screen, Game_name, option_lines, credit_lines, start_menu_scale,
                                        current_state_menu)
    elif current_state == "game":
        if not opengl_initialized:
            start_time = pygame.time.get_ticks()
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.OPENGL | pygame.DOUBLEBUF)
            init_graphics((screen.get_width(), screen.get_height()))
            opengl_initialized = True

            enemies = [Enemy("assets/OBJ/Enemy.obj")]
            untitled_obj = OBJ("assets/OBJ/Map.obj", scale=[1.0, 1.0, 1.0], position=[0, -10.0, 0])
            untitled_obj.generate()
            objects = [untitled_obj,
                       OBJ("assets/OBJ/shotgun.obj", scale=[0.25, 0.25, 0.25], hitbox_size=[0.0, 0.0, 0.0],
                           rotation=[90.0, 0.0, 0.0])]
            player = Player(position=np.array([-109.50993, 0.0, 109.5]), hp=hp_max, ammo=ammo_max)
            hitboxes_map = [
                Hitbox(position=np.array([-193.237, 10.0756, 112.126]), size=np.array([23.687, 60.6338, 175.9088])),
                Hitbox(position=np.array([-19.7332, 10.0756, 112.126]), size=np.array([23.687, 60.6338, 175.90882])),
                Hitbox(position=np.array([-100.0, 10.0756, 22.0]), size=np.array([175.90882, 60.6338, 23.687])),
                Hitbox(position=np.array([-100.0, 10.0756, 195.0]), size=np.array([175.90882, 60.6338, 23.687])),
                Hitbox(position=np.array([-141.76, 3.2, 110.510933]), size=np.array([21.5, 15.5, 21.5])),
                Hitbox(position=np.array([-74.1163, 3.2, 110.510933]), size=np.array([21.5, 15.5, 21.5])),
                Hitbox(position=np.array([-108.50993, 9.7, 110.510933]), size=np.array([50.5, 1.0, 8.5])),
                Hitbox(position=np.array([-109.50993, 1.5, 53.5]), size=np.array([24.0, 9.55143, 2.8])),
                Hitbox(position=np.array([-109.50993, 1.5, 164.5]), size=np.array([24.0, 9.55143, 2.8]))
            ]

            for enemy in enemies:
                enemy.generate()
            for _object in objects:
                _object.generate()
            for hitbox_map in hitboxes_map:
                objects.append(hitbox_map)

            vertices = np.array(untitled_obj.vertices)
            min_x = vertices[:, 0].min()
            max_x = vertices[:, 0].max()
            breite = (max_x - min_x) * untitled_obj.scale[0] - 10.0
            spawn_max_range = breite

            pygame.mouse.set_visible(False)

        dt = clock.tick(60) / 1000.0

        player.handle_events(enemies, current_time)
        if player.flyhack:
            player.handle_flying_movement(dt)
        else:
            player.handle_movement(dt, hitboxes_map)
        player.compute_cam_direction(objects[1])
        player.apply_gravity(hitboxes_map, dt)
        player.apply_transformations()
        player.kill_if_dead(screen_width, screen_height, start_time)
        player.update_positions(objects[1])

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        player.check_collision(enemies, dt, 18)

        if current_time - last_time >= heal_time and player.hp + healing_number <= hp_max:
            player.hp += healing_number
            last_time = current_time

        if current_time - last_spawn_time >= spawn_interval and len(enemies) < max_enemies:
            max_range = 100
            if not np.isfinite(spawn_max_range) or abs(spawn_max_range) > max_range:
                spawn_max_range = max_range
            enemy = Enemy(
                "assets/OBJ/Enemy.obj",
                position=(
                    np.random.uniform(-spawn_max_range / 2, spawn_max_range / 2),
                    -2,
                    np.random.uniform(-spawn_max_range / 2, spawn_max_range / 2)
                )
            )
            enemy.generate()
            enemies.append(enemy)
            last_spawn_time = current_time

        for enemy in enemies:
            enemy.move_to_target(player.position, dt)
            enemy.rotate_to_target(player.position)
            enemy.apply_gravity(objects, dt, player)
            enemy.kill_if_dead(enemies, player)
            if player.hitbox_cheat:
                enemy.hitbox.draw_hitbox((10.0, 10.0, 10.0))
            enemy.render()
            enemy.update_positions()

        for _object in objects:
            if player.hitbox_cheat:
                if isinstance(_object, Hitbox):
                    _object.draw_hitbox((1.0, 1.0, 1.0))
                elif hasattr(_object, "hitbox") and _object.hitbox is not None:
                    _object.hitbox.draw_hitbox((1.0, 1.0, 1.0))
            if hasattr(_object, "render"):
                _object.render()

        # Setup 2D projection für Overlay
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, screen_width, screen_height, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()

        render_text_and_image(screen_width, screen_height)
        if not player.hp <= 0:
            pygame.display.flip()
