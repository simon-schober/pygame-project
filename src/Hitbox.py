import numpy as np
from OpenGL.GL import *


class Hitbox:
    def __init__(self, position, size):
        self.position = np.array(position)  # Mittelpunkt der Hitbox
        self.size = np.array(size)  # Breite, Höhe, Tiefe der Hitbox

    def check_collision(self, other_hitbox):
        # Überprüfen, ob sich die Hitboxen überlappen
        return all(abs(self.position - other_hitbox.position) <= (self.size + other_hitbox.size) / 2)

    def draw_hitbox(self, color):
        x, y, z = self.position
        dx, dy, dz = self.size / 2

        # Aktivieren des Drahtgittermodus
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glColor3f(*color)  # Rot für die Hitbox

        # Zeichne die Box
        glBegin(GL_QUADS)
        # Unterseite
        glVertex3f(x - dx, y - dy, z - dz)
        glVertex3f(x + dx, y - dy, z - dz)
        glVertex3f(x + dx, y - dy, z + dz)
        glVertex3f(x - dx, y - dy, z + dz)
        # Oberseite
        glVertex3f(x - dx, y + dy, z - dz)
        glVertex3f(x + dx, y + dy, z - dz)
        glVertex3f(x + dx, y + dy, z + dz)
        glVertex3f(x - dx, y + dy, z + dz)
        # Vorderseite
        glVertex3f(x - dx, y - dy, z + dz)
        glVertex3f(x + dx, y - dy, z + dz)
        glVertex3f(x + dx, y + dy, z + dz)
        glVertex3f(x - dx, y + dy, z + dz)
        # Rückseite
        glVertex3f(x - dx, y - dy, z - dz)
        glVertex3f(x + dx, y - dy, z - dz)
        glVertex3f(x + dx, y + dy, z - dz)
        glVertex3f(x - dx, y + dy, z - dz)
        # Rechte Seite
        glVertex3f(x + dx, y - dy, z - dz)
        glVertex3f(x + dx, y - dy, z + dz)
        glVertex3f(x + dx, y + dy, z + dz)
        glVertex3f(x + dx, y + dy, z - dz)
        # Linke Seite
        glVertex3f(x - dx, y - dy, z - dz)
        glVertex3f(x - dx, y - dy, z + dz)
        glVertex3f(x - dx, y + dy, z + dz)
        glVertex3f(x - dx, y + dy, z - dz)
        glEnd()

        # Zurücksetzen des Polygonmodus
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def get_collision_vector(self, other_hitbox):
        # Berechnung der Differenz zwischen den Hitboxen
        delta = other_hitbox.position - self.position
        overlap = self.size / 2 + other_hitbox.size / 2 - np.abs(delta)

        # Überprüfung, ob eine Kollision vorliegt
        if np.all(overlap > 0):
            # Kollisionsvektor berechnen (Richtung und Stärke der Kollision)
            collision_vector = np.sign(delta) * overlap
            return collision_vector
        return None

    def check_ray_collision(self, ray_origin, ray_direction):
        # Berechnung der minimalen und maximalen Koordinaten der Hitbox
        min_bound = self.position - self.size / 2
        max_bound = self.position + self.size / 2

        # Initialisiere t_min und t_max
        if not np.any(ray_direction):
            return False
        t_min = (min_bound - ray_origin) / ray_direction
        t_max = (max_bound - ray_origin) / ray_direction

        # Sortiere t_min und t_max
        t1 = np.minimum(t_min, t_max)
        t2 = np.maximum(t_min, t_max)

        # Finde den Eintritts- und Austrittszeitpunkt
        t_enter = np.max(t1)
        t_exit = np.min(t2)

        # Überprüfe, ob der Ray die Hitbox schneidet
        if t_enter <= t_exit and t_exit >= 0:
            return True
        return False
