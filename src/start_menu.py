import pygame
import sys

def make_start_menu():
    pygame.init()
    pygame.font.init()

    Game_name = "Demise"

    # Window
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.toggle_fullscreen()
    pygame.display.set_caption(Game_name)
    # Get screen size
    screen_width, screen_height = screen.get_size()
    surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    
    # Get background picture
    start_bg_picture = pygame.image.load(r"assets\StartMenu\Background\thumb_Doom_1993.jpeg")
    pygame.transform.scale(start_bg_picture, (int(screen_width * 0.27), int(screen_height * 0.27)))

    def Buttons(screen_width):
        def play_button():
            button = pygame.image.load(r'assets\StartMenu\Buttons\play.png')
            return scale_button(button)

        def option_button():
            button = pygame.image.load(r'assets\StartMenu\Buttons\optionen.png')
            return scale_button(button)

        def quit_button():
            button = pygame.image.load(r'assets\StartMenu\Buttons\quit.png')
            return scale_button(button)

        def credits_button():
            button = pygame.image.load(r'assets\StartMenu\Buttons\credits.png')
            return scale_button(button)

        def scale_button(button):
            scaled_button = pygame.transform.scale(button, (int(screen_width * 0.32), int(button.get_height() * int(screen_width * 0.32) / button.get_width())))
            return scaled_button

        play = play_button()
        option = option_button()
        credits = credits_button()
        quit = quit_button()

        return play, option, credits, quit

    def load_and_render_text():
        # Load font
        font = pygame.font.Font(r"assets\StartMenu\Font\BLKCHCRY.TTF", int((280//(screen_height*0.00078125))/2))
        font.set_underline(True)
        font.set_bold(True)
        font.set_italic(True)

        # Rendering text
        text_surface = font.render(Game_name, True, (255, 255, 255))

        # Load and scale texture
        texture = pygame.image.load(r"assets\StartMenu\Rust_Texture\textures\rusty_metal_04_diff_4k.jpg").convert()
        texture = pygame.transform.scale(texture, text_surface.get_size())

        # Create new surface for text with texture
        text_with_texture = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)

        # Apply texture
        text_with_texture.blit(texture, (0, 0))

        # Apply text on top of texture
        text_with_texture.blit(text_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # Set central position
        rect = text_with_texture.get_rect(center=((screen_width//2), 130))
        return text_with_texture, rect

    text_with_texture, rect = load_and_render_text()

    buttons = [play_button, option_button, quit_button, credits_button] = Buttons(screen_width)

    # Main loop
    running = True
    while running:
        # Blit background
        screen.blit(start_bg_picture, (0, 0))

        # Blit transparent surface
        screen.blit(surface, (0, 0))
        for i in range(len(buttons)):
            screen.blit(buttons[i],((screen_width - buttons[i].get_width()) // 2, int(screen_height * 0.6 + i * screen_height * 0.17)-350))

        # Blit text with texture
        screen.blit(text_with_texture, rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    running = False

    pygame.quit()
    sys.exit()