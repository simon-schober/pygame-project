import numpy as np
from OpenGL.GL import *


class Hitbox:
    def __init__(self, position, size=np.array([0.0, 0.0, 0.0])):
        self.position = np.array(position)  # Mittelpunkt der Hitbox
        self.size = np.array(size)  # Breite, Höhe, Tiefe der Hitbox

    def check_collision(self, other_hitbox, player):
        # Überprüfen, ob sich die Hitboxen überlappen
        if not player.colider:
            return all(abs(self.position - other_hitbox.position) <= (self.size + other_hitbox.size) / 2)
        else:
            return False

    def draw_hitbox(self, color):
        x, y, z = self.position
        dx = self.size[0] / 2
        dy = self.size[1] / 2
        dz = self.size[2] / 2

        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glColor3f(*color)

        glBegin(GL_QUADS)

        glVertex3f(x - dx, y - dy, z - dz)
        glVertex3f(x + dx, y - dy, z - dz)
        glVertex3f(x + dx, y - dy, z + dz)
        glVertex3f(x - dx, y - dy, z + dz)

        glVertex3f(x - dx, y + dy, z - dz)
        glVertex3f(x + dx, y + dy, z - dz)
        glVertex3f(x + dx, y + dy, z + dz)
        glVertex3f(x - dx, y + dy, z + dz)

        glVertex3f(x - dx, y - dy, z + dz)
        glVertex3f(x + dx, y - dy, z + dz)
        glVertex3f(x + dx, y + dy, z + dz)
        glVertex3f(x - dx, y + dy, z + dz)

        glVertex3f(x - dx, y - dy, z - dz)
        glVertex3f(x + dx, y - dy, z - dz)
        glVertex3f(x + dx, y + dy, z - dz)
        glVertex3f(x - dx, y + dy, z - dz)

        glVertex3f(x + dx, y - dy, z - dz)
        glVertex3f(x + dx, y - dy, z + dz)
        glVertex3f(x + dx, y + dy, z + dz)
        glVertex3f(x + dx, y + dy, z - dz)

        glVertex3f(x - dx, y - dy, z - dz)
        glVertex3f(x - dx, y - dy, z + dz)
        glVertex3f(x - dx, y + dy, z + dz)
        glVertex3f(x - dx, y + dy, z - dz)
        glEnd()

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def get_collision_vector(self, other_hitbox):
        # Berechnung der Differenz der Positionen der beiden Hitboxen
        # delta ist ein Vektor, der vom aktuellen Objekt zur anderen Hitbox zeigt
        delta = other_hitbox.position - self.position

        # Berechnung der Überlappung (overlap) entlang jeder Achse
        # Die Größe der Hitboxen wird halbiert (Radius) und addiert, um die Summe der "Halbbreiten" zu erhalten
        # Von dieser Summe wird der absolute Wert der Positionsdifferenz subtrahiert,
        # um zu bestimmen, wie viel sich die beiden Hitboxen überlappen
        overlap = self.size / 2 + other_hitbox.size / 2 - np.abs(delta)

        # Prüfen, ob die Überlappung in allen Dimensionen größer als 0 ist
        # np.all(overlap > 0) bedeutet, dass in allen Koordinatenachsen eine Überlappung besteht
        if np.all(overlap > 0):
            # Nur die Achse mit der geringsten Überlappung bestimmen
            min_overlap_axis = np.argmin(overlap)
            collision_vector = np.zeros_like(delta)
            # Richtung beibehalten, aber nur auf der minimalen Achse verschieben
            collision_vector[min_overlap_axis] = np.sign(delta[min_overlap_axis]) * overlap[min_overlap_axis]
            return collision_vector

        # Wenn keine Überlappung in allen Dimensionen vorliegt, keine Kollision => Rückgabe None
        return None

    def check_ray_collision(self, ray_origin, ray_direction):
        # Berechnung der minimalen und maximalen Eckpunkte der Hitbox (AABB - Axis-Aligned Bounding Box)
        # min_bound und max_bound sind die unteren und oberen Grenzen der Hitbox entlang aller Achsen
        min_bound = self.position - self.size / 2
        max_bound = self.position + self.size / 2

        # Wenn der Richtungsvektor des Strahls eine Komponente mit Wert 0 hat,
        # würde eine Division durch 0 in der folgenden Berechnung auftreten,
        # deshalb wird in diesem Fall direkt False zurückgegeben (keine Kollision)
        if not np.all(ray_direction):
            return False

        # Berechnung der Parameter t_min und t_max für die Schnittpunkte des Strahls mit den Bounding Box Ebenen
        # t_min und t_max geben an, wie weit (als Faktor der Richtung) der Strahl gehen muss,
        # um die Min- und Max-Grenzen entlang jeder Achse zu erreichen
        t_min = (min_bound - ray_origin) / ray_direction
        t_max = (max_bound - ray_origin) / ray_direction

        # Sortierung von t_min und t_max, damit t1 immer der Eintrittspunkt (kleinerer Wert)
        # und t2 der Austrittspunkt (größerer Wert) entlang des Strahls ist
        t1 = np.minimum(t_min, t_max)
        t2 = np.maximum(t_min, t_max)

        # Berechnung des maximalen Eintrittspunkts über alle Achsen (t_enter)
        # und des minimalen Austrittspunkts über alle Achsen (t_exit)
        # Dies entspricht dem Intervall auf dem Strahl, in dem er sich innerhalb der Hitbox befindet
        t_enter = np.max(t1)
        t_exit = np.min(t2)

        # Prüfen, ob der Strahl die Hitbox trifft:
        # t_enter <= t_exit bedeutet, dass das Eintrittsintervall nicht nach dem Austrittsintervall liegt
        # t_exit >= 0 bedeutet, dass der Schnittpunkt vor oder am Ursprung des Strahls liegt (nicht "hinter" dem Strahlstart)
        if t_enter <= t_exit and t_exit >= 0:
            # Strahl trifft die Hitbox
            return True

        # Andernfalls keine Kollision
        return False
