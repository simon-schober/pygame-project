import sys

import pygame


def scale_button(button, screen_width):
    return pygame.transform.scale(button,(int(screen_width * 0.32),int(button.get_height() * (screen_width * 0.32) / button.get_width()),),)

def load_buttons(screen_width):
    coppied_buttons = []
    play = scale_button(pygame.image.load(r'assets\StartMenu\Buttons\play.png').convert_alpha() , screen_width)
    option = scale_button(pygame.image.load(r'assets\StartMenu\Buttons\optionen.png').convert_alpha(), screen_width)
    credits = scale_button(pygame.image.load(r'assets\StartMenu\Buttons\credits.png').convert_alpha(), screen_width)
    quit = scale_button(pygame.image.load(r'assets\StartMenu\Buttons\quit.png').convert_alpha(), screen_width)
    return [play, option, credits, quit]


def change_brightness(button, brightness):
    darker_button = button.copy()
    width, height = darker_button.get_size()
    for x in range(0, width, 2):
        for y in range(0, height, 2):
            r, g, b, a = darker_button.get_at((x, y))
            r = max(0, min(255, r + brightness))
            g = max(0, min(255, g + brightness))
            b = max(0, min(255, b + brightness))
            darker_button.set_at((x, y), (r, g, b, a))
    return darker_button

def load_and_render_text(Game_name, screen_width, screen_height):
    font = pygame.font.Font(r"assets\StartMenu\Font\BLKCHCRY.TTF", int((280 // (screen_height * 0.00078125)) / 2))
    font.set_underline(True)
    font.set_bold(True)
    font.set_italic(True)

    text_surface = font.render(Game_name, True, (255, 255, 255))
    texture = pygame.image.load(r"assets\StartMenu\Rust_Texture\textures\rusty_metal_04_diff_4k.jpg").convert()
    texture = pygame.transform.scale(texture, text_surface.get_size())

    text_with_texture = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
    text_with_texture.blit(texture, (0, 0))
    text_with_texture.blit(text_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    rect = text_with_texture.get_rect(center=((screen_width // 2), 130))
    return text_with_texture, rect

def option_menu(screen, screen_width, screen_height, option_lines):
    font = pygame.font.Font(None, int((70 // (screen_height * 0.00078125)) / 2))
    menu_bg_picture = pygame.image.load(r"assets\StartMenu\Stone_Texture\Black_Stone.jpg")
    menu_bg_picture = pygame.transform.scale(menu_bg_picture, (screen_width, screen_height))

    running_options = True
    while running_options:
        screen.blit(menu_bg_picture, (0, 0))
        for i, line in enumerate(option_lines):
            text_surface = font.render(line, False, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(screen_width // 2, 50 + i * 40))
            screen.blit(text_surface, text_rect)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                running_options = False

def credits_menu(screen, screen_width, screen_height, credits_lines):
    font_normal = pygame.font.Font(None, int((70 // (screen_height * 0.00078125)) / 2))
    font_bold_underline = pygame.font.Font(None, int((75 // (screen_height * 0.00078125)) / 2))
    font_bold_underline.set_bold(True)
    font_bold_underline.set_underline(True)

    menu_bg_picture = pygame.image.load(r"assets\StartMenu\Stone_Texture\Black_Stone.jpg")
    menu_bg_picture = pygame.transform.scale(menu_bg_picture, (screen_width, screen_height))

    running_credits = True
    while running_credits:
        screen.blit(menu_bg_picture, (0, 0))
        for i, line in enumerate(credits_lines):
            font = font_bold_underline if i % 2 == 0 else font_normal
            text_surface = font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(screen_width // 2, 50 + i * 40))
            screen.blit(text_surface, text_rect)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                running_credits = False

def make_start_menu(screen, Game_name, option_lines, credits_lines, scale, brightness):
    coppied_button = []

    screen_width, screen_height = screen.get_size()

    start_bg_picture = pygame.image.load(r"assets\StartMenu\Background\thumb_Doom_1993.jpeg")
    start_bg_picture = pygame.transform.scale(start_bg_picture, (screen_width, screen_height))

    buttons = load_buttons(screen_width)
    for button_c in buttons:
        coppied_button.append(button_c.copy())
    text_with_texture, rect = load_and_render_text(Game_name, screen_width, screen_height)

    running = True
    normal = True
    while running:
        screen.blit(start_bg_picture, (0, 0))

        for i, button in enumerate(buttons):
            mouse_pos = pygame.mouse.get_pos()
            x = (screen_width - button.get_width()) // 2
            y = int(screen_height * 0.6 + i * screen_height * 0.17) - 300
            if x <= mouse_pos[0] <= x + button.get_width() and y <= mouse_pos[1] <= y + button.get_height() and normal:
                normal = False
                # Darken the button
                darker_button = change_brightness(button, brightness)
                scaled_button = pygame.transform.smoothscale(darker_button, (int(button.get_width()*scale), int(button.get_height() * scale)))
                screen.blit(scaled_button, ((int(screen_width - scaled_button.get_width()) // 2,int(screen_height * 0.6 + i * screen_height * 0.17) - 350,)))
                print("darker")
            else:
                normal = True
                # Restore the original brightness
                buttons[i] = coppied_button[i].copy()
                screen.blit(button,(int(screen_width - button.get_width()) // 2,int(screen_height * 0.6 + i * screen_height * 0.17) - 350,))


        screen.blit(text_with_texture, rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = event.pos  # Use the position from the event
                for i, button in enumerate(buttons):
                    x = (screen_width - button.get_width()) // 2
                    y = int(screen_height * 0.6 + i * screen_height * 0.17) - 350
                    if button.colidepoint(mouse_pos):
                        if i == 0:  # Play
                            return "game"
                        elif i == 1:  # Options
                            option_menu(screen, screen_width, screen_height, option_lines)
                        elif i == 2:  # Credits
                            credits_menu(screen, screen_width, screen_height, credits_lines)
                        elif i == 3:  # Quit
                            pygame.quit()
                            sys.exit()