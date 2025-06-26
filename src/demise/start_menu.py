import sys

import pygame


def scale_button(button, screen_width):
    return pygame.transform.scale(button, (
        int(screen_width * 0.32), int(button.get_height() * (screen_width * 0.32) / button.get_width())))


def load_buttons(screen_width):
    # Load all the button pictures, und skaliere sie
    play = scale_button(pygame.image.load('assets/2DTexture/StartMenu/Buttons/play.png').convert_alpha(), screen_width)
    option = scale_button(pygame.image.load('assets/2DTexture/StartMenu/Buttons/optionen.png').convert_alpha(),
                          screen_width)
    credits = scale_button(pygame.image.load('assets/2DTexture/StartMenu/Buttons/credits.png').convert_alpha(),
                           screen_width)
    quit = scale_button(pygame.image.load('assets/2DTexture/StartMenu/Buttons/quit.png').convert_alpha(), screen_width)
    dark_button = scale_button(pygame.image.load('assets/2DTexture/StartMenu/Buttons/Dark_Button.png').convert_alpha(),
                               screen_width)
    return [play, option, credits, quit, dark_button]  # dark_button is last!!!


def scale_mouse_texture(mouse_texture, screen_width):
    return pygame.transform.scale(mouse_texture, (
        int(screen_width * 0.035),
        int(mouse_texture.get_height() * (screen_width * 0.035) / mouse_texture.get_width())))


def change_mouse_texture(screen_width):
    return scale_mouse_texture(pygame.image.load(r'assets/2DTexture/StartMenu/MouseSkull.png').convert_alpha(),
                               screen_width)


def change_brightness(button, buttons, scale):
    scaled_button = pygame.transform.smoothscale(buttons[-1],
                                                 (int(button.get_width() * (scale)),
                                                  int(button.get_height() * (scale))))

    return scaled_button


def load_and_render_text(Game_name, screen_width, screen_height):
    # Load a font file, set size based on screen height
    font = pygame.font.Font("assets/Font/BLKCHCRY.TTF", int((140 * ((1.03 / 900) * screen_height))))
    # Make the font underlined, bold, and italic
    font.set_underline(True)
    font.set_bold(True)
    font.set_italic(True)

    # Render the game name text in white
    text_surface = font.render(Game_name, True, (255, 255, 255))
    # Load a rusty metal texture picture and scale it to the size of the text_surface
    texture = pygame.image.load("assets/2DTexture/StartMenu/RustyMetal.png").convert()
    texture = pygame.transform.scale(texture, text_surface.get_size())

    # Create a new transparent surface the same size as the text
    text_with_texture = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
    # Put the rusty texture onto it
    text_with_texture.blit(texture, (0, 0))
    # Put the text on top of the texture, blending them so the texture shows through
    text_with_texture.blit(text_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    # Return the textured text image
    return text_with_texture


def option_menu(screen, screen_width, screen_height, option_lines):
    # Use the default pygame font, scale the size
    font = pygame.font.Font(None, int((60 // (screen_height * 0.00078125)) / 2))
    # Load a background picture for the menu and scale to the creen size
    menu_bg_picture = pygame.image.load("assets/2DTexture/StartMenu/OptionsBackground.png")
    menu_bg_picture = pygame.transform.scale(menu_bg_picture, (screen_width, screen_height))

    running_options = True
    while running_options:
        # Draw the background at (0,0)
        screen.blit(menu_bg_picture, (0, 0))
        # Go through all option lines and draw them on the screen
        for i, line in enumerate(option_lines):
            text_surface = font.render(line, False, (255, 255, 255))
            text_rect = text_surface.get_rect()
            # Put each line at x = center - 250, y starts at 50 and goes down by 40 each time
            text_rect.topleft = (screen_width // 2 - 250, 50 + i * 40)
            screen.blit(text_surface, text_rect)

        pygame.display.flip()  # Update what is shown on the screen

        # Check for events like closing the window or pressing ESC
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                running_options = False  # Exit the options menu


def credits_menu(screen, screen_width, screen_height, credits_lines):
    # Set up two fonts: normal size and a bold, underlined size, both scaled
    font_normal = pygame.font.Font(None, int((70 // (screen_height * 0.00078125)) / 2))
    font_bold_underline = pygame.font.Font(None, int((75 // (screen_height * 0.00078125)) / 2))
    font_bold_underline.set_bold(True)
    font_bold_underline.set_underline(True)

    # Load and scale the same background picture as options menu
    menu_bg_picture = pygame.image.load("assets/2DTexture/StartMenu/OptionsBackground.png")
    menu_bg_picture = pygame.transform.scale(menu_bg_picture, (screen_width, screen_height))

    running_credits = True
    while running_credits:
        # Draw the background
        screen.blit(menu_bg_picture, (0, 0))
        # Go through each line of credits
        for i, line in enumerate(credits_lines):
            # Use bold+underline font for every 3rd line (and if i < 13) or if it is the first line else use normal font
            font = font_bold_underline if ((i + 1) % 3 == 0 and i < 13) or i == 0 else font_normal
            text_surface = font.render(line, True, (255, 255, 255))  # white text
            # Center each line horizontally, y starts at 50 and goes down by 40 each time
            text_rect = text_surface.get_rect(center=(screen_width // 2, 50 + i * 40))
            screen.blit(text_surface, text_rect)

        pygame.display.flip()  # Update the screen

        # Check for quitting or pressing ESC to exit credits menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                running_credits = False  # Exit credits menu


def make_start_menu(screen, Game_name, option_lines, credits_lines, scale, current_state_menu):
    # Get the width and height of the window
    screen_width, screen_height = screen.get_size()

    # Makes a new mouse texture
    mouse_texture = change_mouse_texture(screen_width)
    # Load and scale the background image for the start menu
    start_bg_picture = pygame.image.load("assets/2DTexture/StartMenu/StartMenuBackground.png")
    start_bg_picture = pygame.transform.scale(start_bg_picture, (screen_width, screen_height))

    # Load buttons and the dark overlay
    buttons = load_buttons(screen_width)
    # Load the game name text with rusty texture
    text_with_texture = load_and_render_text(Game_name, screen_width, screen_height)

    running = True
    while running:
        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()
        # Draw the background, mouse texture and text texture each frame
        screen.blit(start_bg_picture, (0, 0))
        screen.blit(text_with_texture, (((screen_width - text_with_texture.get_width()) // 2), 0))
        was_clicked = False
        which_button = None
        for i, button in enumerate(buttons[:len(buttons) - 1]):
            if (
                    ((screen_width - button.get_width()) // 2 + int(90 * scale) < mouse_pos[0] < (
                            screen_width + button.get_width()) // 2 - int(75 * scale))
                    and
                    (int(screen_height * 0.6 + i * screen_height * 0.17) - int(280 * scale) < mouse_pos[1] < int(
                        screen_height * 0.6 + i * screen_height * 0.17) - int(140 * scale))
            ):

                was_clicked = True
                which_button = i
                # If the mouse is over the button, darken it and make it slightly bigger
                darker_button = change_brightness(button, buttons, 1.05)

                scaled_button = pygame.transform.smoothscale(button, (
                    int(button.get_width() * (1.05)),
                    int(button.get_height() * (1.05)
                        )))

                screen.blit(scaled_button, ((screen_width - scaled_button.get_width()) // 2,
                                            int(screen_height * 0.6 + i * screen_height * 0.17) - int(scale * 380)))

                screen.blit(darker_button, ((screen_width - scaled_button.get_width()) // 2,
                                            int(screen_height * 0.6 + i * screen_height * 0.17) - int(scale * 380)))
            else:
                # If the mouse is not over it, just draw the normal button
                screen.blit(button, ((int(screen_width - button.get_width()) // 2),
                                     (int(screen_height * (0.6 + i * 0.17)) - int(380 * scale))))
            # Watch for any key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and was_clicked:
                # If we are on the main menu, look which button was clicked
                if current_state_menu == "main":
                    if which_button == 0:  # "Play" button
                        running = False
                        return "game"
                    elif which_button == 1:  # Options button
                        current_state_menu = "options"
                    elif which_button == 2:  # Credits button
                        current_state_menu = "credits"
                    elif which_button == 3:  # Quit button
                        pygame.quit()
                        sys.exit()
        if current_state_menu == "options":
            option_menu(screen, screen_width, screen_height, option_lines)
            current_state_menu = "main"
        elif current_state_menu == "credits":
            credits_menu(screen, screen_width, screen_height, credits_lines)
            current_state_menu = "main"
        screen.blit(mouse_texture, (mouse_pos[0] - 10, mouse_pos[1] - 3))
        pygame.display.flip()  # Show all the draws on the screen

# About 118 lines of code
