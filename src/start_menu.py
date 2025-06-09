import sys
import pygame

def scale_button(button, screen_width):
    return pygame.transform.scale(button,(int(screen_width * 0.32),int(button.get_height() * (screen_width * 0.32) / button.get_width()),),)

def load_buttons(screen_width):
    #Load all the button pictures, and scale it
    play = scale_button(pygame.image.load(r'assets\StartMenu\Buttons\play.png').convert_alpha(), screen_width)
    option = scale_button(pygame.image.load(r'assets\StartMenu\Buttons\optionen.png').convert_alpha(),screen_width)
    credits = scale_button(pygame.image.load(r'assets\StartMenu\Buttons\credits.png').convert_alpha(),screen_width)
    quit = scale_button(pygame.image.load(r'assets\StartMenu\Buttons\quit.png').convert_alpha(),screen_width)
    dark_button = scale_button(pygame.image.load(r'assets\StartMenu\Buttons\Dark_Button.png').convert_alpha(),screen_width)
    
    #Make a new surface the same size as dark_button, with transparency support (SRCALPHA)
    surface = pygame.Surface((dark_button.get_width(), dark_button.get_height()),pygame.SRCALPHA)
    #Fill that surface with black and make it see-through a bit (alpha = 100)
    surface.fill((0, 0, 0, 100))

    #Return a list of the button images plus the dark overlay surface
    return [play, option, credits, quit, dark_button], surface  #dark_button is last!!!

def scale_mouse_texture(mouse_texture, screen_width):
    return	pygame.transform.scale(mouse_texture, (int(screen_width * 0.035), int(mouse_texture.get_height() * (screen_width * 0.035) / mouse_texture.get_width())))

def change_mouse_texture(screen_width):
    return scale_mouse_texture(pygame.image.load(r'assets\StartMenu\Mouse_texture\Mouse_skull.png').convert_alpha(), screen_width)


def change_brightness(button, buttons, surface, screen_width, screen_height, scale, i):
    #Take the last image in buttons (dark_button) and resize it to match the hovered button size
    scaled_button = pygame.transform.smoothscale(buttons[-1],(int(button.get_width() * scale),int(button.get_height() * scale)))
    #Put the dark overlay on top of the button at the correct position
    surface.blit(scaled_button,((int(screen_width - button.get_width()) // 2),(int(screen_height * 0.6 + i * screen_height * 0.17) - 350),),)
    #Return the dark overlay picture we just made
    return scaled_button

def load_and_render_text(Game_name, screen_width, screen_height):
    #Load a font file, set size based on screen height
    font = pygame.font.Font(r"assets\StartMenu\Font\BLKCHCRY.TTF",int((280 // (screen_height * 0.00078125)) / 2))
    #Make the font underlined, bold, and italic
    font.set_underline(True)
    font.set_bold(True)
    font.set_italic(True)

    #Render the game name text in white
    text_surface = font.render(Game_name, True, (255, 255, 255))
    #Load a rusty metal texture picture and resize it to the text size
    texture = pygame.image.load(r"assets\StartMenu\Rust_Texture\textures\rusty_metal_04_diff_4k.jpg").convert()
    texture = pygame.transform.scale(texture, text_surface.get_size())

    #Create a new transparent surface the same size as the text
    text_with_texture = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
    #Put the rusty texture onto it
    text_with_texture.blit(texture, (0, 0))
    #Put the text on top of the texture, blending them so the texture shows through
    text_with_texture.blit(text_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    #Get a rectangle for the text and center it at the top of the screen (y = 130)
    rect = text_with_texture.get_rect(center=((screen_width // 2), 130))
    #Return the textured text image and its rectangle
    return text_with_texture, rect

def option_menu(screen, screen_width, screen_height, option_lines):
    #Use the default pygame font, scale size by screen height
    font = pygame.font.Font(None, int((60 // (screen_height * 0.00078125)) / 2))
    #Load a background picture for the menu and scale to screen size
    menu_bg_picture = pygame.image.load(r"assets\StartMenu\Stone_Texture\Black_Stone.jpg")
    menu_bg_picture = pygame.transform.scale(menu_bg_picture, (screen_width, screen_height))

    running_options = True
    while running_options:
        #Draw the background at (0,0)
        screen.blit(menu_bg_picture, (0, 0))
        #Go through all option lines and draw them on the screen
        for i, line in enumerate(option_lines):
            text_surface = font.render(line, False, (255, 255, 255))  #white text
            text_rect = text_surface.get_rect()
            #Put each line at x = center - 250, y starts at 50 and goes down by 40 each time
            text_rect.topleft = (screen_width // 2 - 250, 50 + i * 40)
            screen.blit(text_surface, text_rect)

        pygame.display.flip()  #Update what is shown on the screen

        #Check for events like closing the window or pressing ESC
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                running_options = False  #Exit the options menu

def credits_menu(screen, screen_width, screen_height, credits_lines):
    #Set up two fonts: normal size and a bold, underlined size, both scaled by screen height
    font_normal = pygame.font.Font(None, int((70 // (screen_height * 0.00078125)) / 2))
    font_bold_underline = pygame.font.Font(None, int((75 // (screen_height * 0.00078125)) / 2))
    font_bold_underline.set_bold(True)
    font_bold_underline.set_underline(True)

    #Load and scale the same background picture as options menu
    menu_bg_picture = pygame.image.load(r"assets\StartMenu\Stone_Texture\Black_Stone.jpg")
    menu_bg_picture = pygame.transform.scale(menu_bg_picture, (screen_width, screen_height))

    running_credits = True
    while running_credits:
        #Draw the background
        screen.blit(menu_bg_picture, (0, 0))
        #Go through each line of credits
        for i, line in enumerate(credits_lines):
            #Use bold+underline font for every 3rd line (and if i < 13) or if it is the first line else use normal font
            font = font_bold_underline if ((i + 1) % 3 == 0 and i < 13) or i == 0 else font_normal
            text_surface = font.render(line, True, (255, 255, 255))  #white text
            #Center each line horizontally, y starts at 50 and goes down by 40 each time
            text_rect = text_surface.get_rect(center=(screen_width // 2, 50 + i * 40))
            screen.blit(text_surface, text_rect)

        pygame.display.flip()  #Update the screen

        #Check for quitting or pressing ESC to exit credits menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                running_credits = False  #Exit credits menu

def make_start_menu(screen, Game_name, option_lines, credits_lines, scale, current_state_menu):
    #Get the width and height of the window
    screen_width, screen_height = screen.get_size()

    #Makes a new mouse texture
    mouse_texture = change_mouse_texture(screen_width)
    #Load and scale the background image for the start menu
    start_bg_picture = pygame.image.load(r"assets\StartMenu\Background\thumb_Doom_1993.jpeg")
    start_bg_picture = pygame.transform.scale(start_bg_picture, (screen_width, screen_height))

    #Load buttons and the dark overlay using our load_buttons function
    buttons, surface = load_buttons(screen_width)
    #Load the game name text with rusty texture
    text_with_texture, rect = load_and_render_text(Game_name, screen_width, screen_height)

    running = True
    while running:
        #Draw the background each frame
        screen.blit(start_bg_picture, (0, 0))

        #Go through each button except the last one (which is the dark overlay)
        for i, button in enumerate(buttons[:len(buttons) - 1]):
            mouse_pos = pygame.mouse.get_pos()  #Get the position of the mouse cursor
            #Make a rectangle for the button to check later if button and cursor are at the same position
            if ((screen_width - button.get_width()) // 2 +90 < mouse_pos[0] < (screen_width + button.get_width()) // 2 -75 and int(screen_height * 0.6 + i * screen_height * 0.17) - 280 < mouse_pos[1] < int(screen_height * 0.6 + i * screen_height * 0.17) - 140):
                #If the mouse is over the button, darken it and make it slightly bigger
                darker_button = change_brightness(button, buttons, surface, screen_width, screen_height, scale, i)
                scaled_button = pygame.transform.smoothscale(button,(int(button.get_width() * scale),int(button.get_height() * scale)))
                #Draw the bigger button first
                screen.blit(scaled_button,((int(screen_width - scaled_button.get_width()) // 2),(int(screen_height * 0.6 + i * screen_height * 0.17) - 350),))
                #Draw the dark overlay on top
                screen.blit(darker_button,((int(screen_width - scaled_button.get_width()) // 2),(int(screen_height * 0.6 + i * screen_height * 0.17) - 350)))
            else:
                #If the mouse is not over it, just draw the normal button
                screen.blit(button,((int(screen_width - button.get_width()) // 2),(int(screen_height * 0.6 + i * screen_height * 0.17) - 350),))

        #Draw the game name text with texture on top of everything
        screen.blit(mouse_texture, (mouse_pos[0]-10, mouse_pos[1]-3))
        screen.blit(text_with_texture, rect)
        pygame.display.flip()  #Show all the drawn stuff on the screen
        #Check for events like clicks or quitting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  #Left-click released
                mouse_pos = event.pos  #Get click position

                #Check each button to see if it was clicked
                for i, button in enumerate(buttons[:len(buttons) - 1]):
                    if ((screen_width - button.get_width()) // 2 +90 < mouse_pos[0] < (screen_width + button.get_width()) // 2 -75 and int(screen_height * 0.6 + i * screen_height * 0.17) - 280 < mouse_pos[1] < int(screen_height * 0.6 + i * screen_height * 0.17) - 140):                    
                        #If we are on the main menu, figure out which button was clicked
                        if current_state_menu == "main":
                            if i == 0:  #"Play" button
                                running = False
                                return "game"
                            elif i == 1:  #Options button
                                current_state_menu = "options"
                            elif i == 2:  #Credits button
                                current_state_menu = "credits"
                            elif i == 3:  #Quit button
                                pygame.quit()
                                sys.exit()
                        #If we are in the options menu, show it
            if current_state_menu == "options":
                option_menu(screen, screen_width, screen_height, option_lines)
                current_state_menu = "main"
            #If we are in the credits menu, show it
            elif current_state_menu == "credits":
                credits_menu(screen, screen_width, screen_height, credits_lines)
                current_state_menu = "main"

#about 130 lines of code Finally my work is don it took me abou a week to winish everything