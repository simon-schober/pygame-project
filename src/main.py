from Enemy import *
from OBJ import *
from Player import Player
from graphics import init_graphics
from start_menu import make_start_menu

# Menu variables
Game_name = "Demise"
option_lines = [
    "Options:", "Move: ", "W          -->     Move forward", "",
    "A          -->     Move Left", "", "S          -->     Move Backwards", "",
    "D          -->     Move Right", "", "Move Mouse  -->     Rotate your Character", "",
    "Left click -->     Shoot with Gun", "",
    "You can't change the Keybinds", "",
    "Tip: You can always press ESC-Key ", "to leave the game (The score doesn't get saved)", "",
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

# Initialize screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF)
pygame.display.set_caption(Game_name)
screen_width, screen_height = screen.get_size()
start_menu_scale = 1.03 / 900 * screen_height
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
max_enemies = 10

# Create font for the HP bar
hp_font = pygame.font.Font("assets/StartMenu/Font/BLKCHCRY.TTF", 145)


def render_2D_texture(surface, x, y, screen_width, screen_height):
    texture_data = pygame.image.tostring(surface, "RGBA", True)
    width, height = surface.get_size()

    # Hintergrundfarbe setzen, falls nicht geschehen (optional)
    glClearColor(0.1, 0.1, 0.1, 1.0)  # Dunkelgrau statt Schwarz

    # Zustand speichern
    glPushAttrib(GL_ENABLE_BIT)

    # Wichtig: Beleuchtung deaktivieren (falls aktiv)
    glDisable(GL_LIGHTING)

    # Tiefentest deaktivieren für 2D Overlays
    glDisable(GL_DEPTH_TEST)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    # Wechsel in 2D-Orthoprojektion
    # Setting up a new projection matrix and setting it to Orthographic
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()  # Pushing a new matrix to the stack -> Creating a new one
    glLoadIdentity()  # Metaphorically settting matrix to 1
    glOrtho(0, screen_width, screen_height, 0, -1,
            1)  # Setting up the Orthographic perspective (This is always done with multiplying)
    # So we needed to set the matrix to 1 before

    # Setting up a new modelview matrix
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glEnable(GL_TEXTURE_2D)  # Enabling textures
    glBindTexture(GL_TEXTURE_2D, texture_id)  # Binding our texture to draw with
    glBegin(GL_QUADS)  # Start drawing

    # Drawing a simple square
    glTexCoord2f(0, 1);
    glVertex2f(x, y)
    glTexCoord2f(1, 1);
    glVertex2f(x + width, y)
    glTexCoord2f(1, 0);
    glVertex2f(x + width, y + height)
    glTexCoord2f(0, 0);
    glVertex2f(x, y + height)

    # Ending the drawing
    glEnd()
    glDisable(GL_TEXTURE_2D)  # Disabling textures

    # Popping the matrices we created before to continue drawing normally
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

    glDeleteTextures([texture_id])
    glDisable(GL_BLEND)

    # Vorherige OpenGL-Zustände wiederherstellen
    glPopAttrib()


def render_text_and_image(screen_width, screen_height):
    hp_bar_field = pygame.image.load('assets/Game/Hp_bar_texture.png').convert_alpha()
    hp_bar_field = pygame.transform.smoothscale(hp_bar_field, (
        int(screen_width * 0.32), int(hp_bar_field.get_height() * (screen_width * 0.32) / hp_bar_field.get_width())))
    render_2D_texture(hp_bar_field, 10, 10, screen_width, screen_height)

    hp_surface = pygame.Surface((330, 55), pygame.SRCALPHA)
    pygame.draw.rect(hp_surface, (53, 211, 2) if player.hp > 155 else (254, 102, 5) if player.hp > 100 else (
        (138, 5, 6) if player.hp > 45 else (70, 5, 5)), (0, 0, 330 * (player.hp / hp_max), 55))
    render_2D_texture(hp_surface, 110, 100, screen_width, screen_height)

    crosshair = pygame.image.load('assets/Game/crosshair.png').convert_alpha()
    crosshair = pygame.transform.smoothscale(crosshair, (
        int(screen_width * 0.01), int(hp_bar_field.get_height() * (screen_width * 0.015) / hp_bar_field.get_width())))
    render_2D_texture(crosshair, (screen_width - crosshair.get_width()) // 2,
                      (screen_height - crosshair.get_height()) // 2, screen_width, screen_height)
    # Text rendern
    hp_font = pygame.font.Font('assets/StartMenu/Font/BLKCHCRY.TTF', int((175 // (screen_height * 0.00078125)) / 2))
    text_surface = hp_font.render(f"{int(player.hp)}", True, (97, 93, 87))
    render_2D_texture(text_surface, 270, 140, screen_width, screen_height)
    # Bullet_rander
    bullet_font = pygame.font.Font('assets/StartMenu/Font/BLKCHCRY.TTF', int((100 // (screen_height * 0.00078125)) / 2))
    text_surface = bullet_font.render(f"{int(player.ammo)}/{ammo_max}", True, (97, 93, 87))
    render_2D_texture(text_surface, screen_width - 300, 140, screen_width, screen_height)
    # Magazin-Counter direkt darunter anzeigen
    mag_surface = bullet_font.render(f"{int(player.mag_ammo)}/{int(player.mag_size)}", True, (200, 200, 200))
    render_2D_texture(mag_surface, screen_width - 300, 210, screen_width, screen_height)
    bullet_pic = pygame.image.load("assets/Game/ammo-rifle.png").convert_alpha()
    bullet_pic = pygame.transform.smoothscale(bullet_pic, (
        int(screen_width * 0.1), int(hp_bar_field.get_height() * (screen_width * 0.17) / hp_bar_field.get_width())))
    render_2D_texture(bullet_pic, screen_width - 300, -10, screen_width, screen_height)


# Main loop
pygame.mouse.set_visible(False)
while True:
    current_time = pygame.time.get_ticks()
    if current_state == "menu":
        current_state = make_start_menu(screen, Game_name, option_lines, credit_lines, start_menu_scale,
                                        current_state_menu)
    elif current_state == "game":
        if not opengl_initialized:
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.OPENGL | pygame.DOUBLEBUF)
            init_graphics((screen.get_width(), screen.get_height()))
            opengl_initialized = True

            enemies = [Enemy("assets/OBJ/Enemy.obj")]
            player = Player(position=np.array([0.0, 20.0, 10.0]), hp=hp_max, ammo=ammo_max)
            objects = [OBJ("assets/OBJ/Plane.obj", scale=[3.0, 3.0, 3.0], hitbox_size=np.array([350.0, 1.0, 350.0])),
                       OBJ("assets/OBJ/pistol_new_texture.obj", scale=[5.0, 5.0, 5.0])]

            for enemy in enemies:
                enemy.generate()
            for _object in objects:
                _object.generate()

            pygame.mouse.set_visible(False)

        dt = clock.tick(60) / 1000.0

        player.handle_events(enemies, current_time)
        if player.flyhack:
            player.handle_flying_movement(dt)
        else:
            player.handle_movement(dt)
        player.compute_cam_direction(objects[1])
        player.apply_gravity(objects, dt)
        player.apply_transformations()
        player.kill_if_dead()
        player.update_positions(objects[1])

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        player.check_collision(enemies, dt)

        if current_time - last_time >= heal_time and player.hp + healing_number <= hp_max:
            player.hp += healing_number
            last_time = current_time

        if current_time - last_spawn_time >= spawn_interval and len(enemies) < max_enemies:
            enemy = Enemy("assets/OBJ/Enemy.obj", position=(np.random.random(3) * 200) - 100)
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
                _object.hitbox.draw_hitbox((10.0, 10.0, 10.0))
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
        pygame.display.flip()
