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
        # Berechnung des Kollisionsvektors:
        # np.sign(delta) gibt für jede Komponente +1 oder -1 zurück, je nachdem, in welche Richtung die andere Hitbox liegt
        # Multipliziert mit overlap, gibt dies den Vektor der minimalen Verschiebung, 
        # um die Hitboxen aus der Überlappung zu bringen
        collision_vector = np.sign(delta) * overlap
        
        # Rückgabe des Kollisionsvektors, der Richtung und Stärke der Kollision repräsentiert
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
