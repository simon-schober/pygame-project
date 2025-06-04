import pygame

# Pygame initialisieren
pygame.init()

# Fenstergröße und Anzeige
screen_width, screen_height = 600, 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Button mit Hover-Effekt")

# Farben definieren
WHITE = (255, 255, 255)
BUTTON_COLOR = (70, 130, 180)  # Stahlblau
TEXT_COLOR = (255, 255, 255)

# Schriftart laden
font = pygame.font.SysFont(None, 36)

# Button-Text rendern
text_surface = font.render("Klick mich!", True, TEXT_COLOR)

# Button-Größe basierend auf Textgröße
button_width = text_surface.get_width() + 40
button_height = text_surface.get_height() + 20

# Button-Position
button_x = (screen_width - button_width) // 2
button_y = (screen_height - button_height) // 2

# Button-Rechteck
button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

# Funktion zum Erstellen des Button-Surface
def create_button_surface(color):
    surface = pygame.Surface((button_width, button_height))
    surface.fill(color)
    surface.blit(text_surface, ((button_width - text_surface.get_width()) // 2,
                                (button_height - text_surface.get_height()) // 2))
    return surface

# Ursprüngliches Button-Surface
button_surface = create_button_surface(BUTTON_COLOR)

# Abdunkelungssurface für Hover-Effekt
darken_surface = pygame.Surface((button_width, button_height))
darken_surface.fill((30, 30, 30))  # Abdunkelung um 30 bei jedem RGB-Kanal

# Haupt-Loop
running = True
while running:
    screen.fill(WHITE)

    # Mausposition abrufen
    mouse_pos = pygame.mouse.get_pos()

    # Überprüfen, ob Maus über dem Button ist
    if button_rect.collidepoint(mouse_pos):
        # Kopie des Button-Surface erstellen
        hovered_button = button_surface.copy()
        # Abdunkelung anwenden
        hovered_button.blit(darken_surface, (0, 0), special_flags=pygame.BLEND_RGB_SUB)
        # Button anzeigen
        screen.blit(hovered_button, button_rect.topleft)
    else:
        # Ursprünglichen Button anzeigen
        screen.blit(button_surface, button_rect.topleft)

    # Ereignisse verarbeiten
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Anzeige aktualisieren
    pygame.display.flip()

# Pygame beenden
pygame.quit()
