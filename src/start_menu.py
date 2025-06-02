import pygame
import sys

pygame.init()

# Window
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.toggle_fullscreen()
pygame.display.set_caption("Doom 2.0")

# Get screen size
screen_width, screen_height = screen.get_size()

surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)

# Get background picture
start_bg_picture = pygame.image.load(r"assets\Grafik_start_menu\Background\thumb_Doom_1993.jpeg")

def transparence_menu():
    #create rectangle for the menu
    pygame.draw.rect(surface, (255, 255, 255, 120), [450, 400, 1100, 570])

def Butons():
    #defs to load the images
    def play_buttons():
        play_button = pygame.image.load(r'assets\Grafik_start_menu\Buttons\play.png')
        return play_button
    def option_buttons():
            option_button = pygame.image.load(r'assets\Grafik_start_menu\Buttons\optionen.png')
            return option_button
    def quit_buttons():
            quit_button = pygame.image.load(r'assets\Grafik_start_menu\Buttons\quit.png')
            return quit_button
    def credits_buttons():
            credits_button = pygame.image.load(r'assets\Grafik_start_menu\Buttons\credits.png')
            return credits_button

    play_button = play_buttons()
    option_button = option_buttons()
    quit_button = quit_buttons()
    credits_button = credits_buttons()

    return play_button, option_button, quit_button, credits_button

def load_and_render_text():
    # Load font
    font = pygame.font.Font(r"assets\Grafik_start_menu\Font\BLKCHCRY.TTF", 280)
    font.set_underline(True)
    font.set_bold(True)
    font.set_italic(True)

    # Rendering text
    text = "Doom 2.0"
    text_surface = font.render(text, True, (255, 255, 255))

    # Load and scale texture
    texture = pygame.image.load(r"assets\Grafik_start_menu\Rust_Texture\textures\rusty_metal_04_diff_4k.jpg").convert()
    texture = pygame.transform.scale(texture, text_surface.get_size())

    # Create new surface for text with texture
    text_with_texture = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)

    # Apply texture
    text_with_texture.blit(texture, (0, 0))

    # Apply text on top of texture
    text_with_texture.blit(text_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    # Set central position
    rect = text_with_texture.get_rect(center=(1000, 200))
    return text_with_texture, rect

text_with_texture, rect = load_and_render_text()

transparence_menu()

buttons = [play_button, option_button, quit_button, credits_button] = Butons()

# Main loop
running = True
while running:
    # Blit background
    screen.blit(start_bg_picture, (0, 0))

    # Blit transparent surface
    screen.blit(surface, (0, 0))
    for i in range(len(buttons)):
        screen.blit(buttons[i], (750,330+i*143))
    # Blit text with texture
    screen.blit(text_with_texture, rect)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                running = False

pygame.quit()
sys.exit()