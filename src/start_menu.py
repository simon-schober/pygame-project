import pygame
import sys

def make_start_menu(Game_name):
    pygame.init()
    pygame.font.init()

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

    def option_menu(screen, screen_width, screen_height):
            pygame.font.init()
            font = pygame.font.Font(None, int((70//(screen_height*0.00078125))/2))
            option_lines = [
                "Optins:",
                "",
                "Bewegen: ",
                "W          -->     Move vorward",
                "A          -->     Move Left",
                "S          -->     Move Backwards",
                "D          -->     Move Right",
                "Move Mous  -->     Rotate your Cracter",
                "Left Klick -->     Shoot with Gun"
                "",
                "You can`t change the Keybinds",
                "",
                "Press Arrow-Down-Key To go back to the menu"
            ]
            running = True
            y_start = 50
            line_height = 40
                
            menu_bg_picture = pygame.image.load(r"assets\StartMenu\Stone_Texture\Black_Stone.jpg")
            pygame.transform.scale(menu_bg_picture, (int(screen_width * 0.27), int(screen_height * 0.27)))
            while running:
                screen.blit(menu_bg_picture, (0, 0))

                for i in range(len(option_lines)):
                    text_surface = font.render(option_lines[i], True, (255, 255, 255))
                    text_rect = text_surface.get_rect(center=(screen_width // 2, y_start + i * line_height))
                    screen.blit(text_surface, text_rect)
                
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN:
                            running = False

    def credits_menu(screen, screen_width, screen_height):
        pygame.font.init()
        credits_lines = [
            "Credits:",
            "",
            "Programmierung: ",
            "Alexander Sief & Simon Schober",
            "Grafik: ",
            "   Vladimir Kandalintsev",
            "Sound: ",
            "   Simon Schober",
            "",
            "♥ Thx for playing our Game ♥",
            "",
            "Press Arrow-Down-Key To go back to the menu"
        ]
        running = True
        y_start = 50
        line_height = 40
            
        menu_bg_picture = pygame.image.load(r"assets\StartMenu\Stone_Texture\Black_Stone.jpg")
        pygame.transform.scale(menu_bg_picture, (int(screen_width * 0.27), int(screen_height * 0.27)))
        font_normal = pygame.font.Font(None, int((70//(screen_height*0.00078125))/2))
        font_bold_underline = pygame.font.Font(None, int((75//(screen_height*0.00078125))/2))
        font_bold_underline.set_bold(True)
        font_bold_underline.set_underline(True)
        while running:
            screen.blit(menu_bg_picture, (0, 0))

            for i in range(len(credits_lines)):
                if i % 2 == 0:
                    text_surface = font_bold_underline.render(credits_lines[i], True, (255, 255, 255))
                else:
                    text_surface = font_normal.render(credits_lines[i], True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(screen_width // 2, y_start + i * line_height))
                screen.blit(text_surface, text_rect)
            
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        running = False


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
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    
            if event.type == pygame.MOUSEBUTTONUP:
                mouse = pygame.mouse.get_pos()
                for i in range(len(buttons)):
                    button = buttons[i]
                    x = (screen_width - button.get_width()) // 2
                    y = int(screen_height * 0.6 + i * screen_height * 0.17) - 350
                    if x <= mouse[0] <= x + button.get_width() and y <= mouse[1] <= y + button.get_height():
                        if button == buttons[0]:
                            running = False
                        if button == buttons[1]:
                            option_menu(screen, screen_width, screen_height)
                        if button == buttons[2]:
                            credits_menu(screen, screen_width, screen_height)
                        if button == buttons[3]:
                            pygame.quit()
                            sys.exit()