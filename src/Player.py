"""
Player-Modul
============

Dieses Modul enthält die Player-Klasse für das Spiel.
"""

import sys
from copy import copy

import numpy as np
import pygame
from OpenGL.GL import *
from pygame import *

from Hitbox import Hitbox


def clamp(x, minimum, maximum):
    """Begrenzt x auf den Bereich [minimum, maximum]."""
    return max(minimum, min(x, maximum))


def render_2D_texture(surface, x, y, screen_width, screen_height):
    texture_data = pygame.image.tostring(surface, "RGBA", True)
    width, height = surface.get_size()

    # Hintergrundfarbe setzen, falls nicht geschehen (optional)
    glClearColor(0.1, 0.1, 0.1, 1.0)  # Dunkelgrau statt Schwarz

    # Zustand speichern
    glPushAttrib(GL_ENABLE_BIT)

    # Wichtig: Beleuchtung deaktivieren (falls aktiv)
    glDisable(GL_LIGHTING)

    # Tiefentest deaktivieren für 2D Overlays
    glDisable(GL_DEPTH_TEST)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    # Wechsel in 2D-Orthoprojektion
    # Setting up a new projection matrix and setting it to Orthographic
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()  # Pushing a new matrix to the stack -> Creating a new one
    glLoadIdentity()  # Metaphorically settting matrix to 1
    glOrtho(0, screen_width, screen_height, 0, -1,
            1)  # Setting up the Orthographic perspective (This is always done with multiplying)
    # So we needed to set the matrix to 1 before

    # Setting up a new modelview matrix
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glEnable(GL_TEXTURE_2D)  # Enabling textures
    glBindTexture(GL_TEXTURE_2D, texture_id)  # Binding our texture to draw with
    glBegin(GL_QUADS)  # Start drawing

    # Drawing a simple square
    glTexCoord2f(0, 1);
    glVertex2f(x, y)
    glTexCoord2f(1, 1);
    glVertex2f(x + width, y)
    glTexCoord2f(1, 0);
    glVertex2f(x + width, y + height)
    glTexCoord2f(0, 0);
    glVertex2f(x, y + height)

    # Ending the drawing
    glEnd()
    glDisable(GL_TEXTURE_2D)  # Disabling textures

    # Popping the matrices we created before to continue drawing normally
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

    glDeleteTextures([texture_id])
    glDisable(GL_BLEND)

    # Vorherige OpenGL-Zustände wiederherstellen
    glPopAttrib()


class Player:
    def __init__(self, position=None, rx=0, ry=0, move_speed=50, gravity=20,
                 direction=None, up=None, hitbox_size=None, hp=200.0, ammo=100,
                 velocity=None, acceleration=None, friction=0.95, max_speed=500.0):
        # Standardwerte für numpy-Arrays
        self.position = np.array([0.0, 10.0, 0.0]) if position is None else position
        self.direction = np.array([1.0, 0.0, 0.0]) if direction is None else direction
        self.up = np.array([0.0, 1.0, 0.0]) if up is None else up
        self.hitbox_size = np.array([5.0, 4.0, 5.0]) if hitbox_size is None else hitbox_size
        self.velocity = np.array([0.0, 0.0, 0.0]) if velocity is None else velocity
        self.acceleration = np.array([0.0, 0.0, 0.0]) if acceleration is None else acceleration
        self.rx = rx
        self.ry = ry
        self.right = np.cross(self.direction, self.up)
        self.right = self.right / np.linalg.norm(self.right)
        self.move_speed = move_speed
        self.gravity = gravity
        self.friction = friction
        self.max_speed = max_speed
        self.hp = hp
        self.ammo = ammo
        self.hitbox_cheat = False
        self.flyhack = False
        self.healhack = False
        self.infinity = False
        self.colider = False
        self.godmode_sequence = []
        self.last_input_time = 0
        self.godmode_code = ['up', 'left', 'down', 'right']
        self.footstep_sound = pygame.mixer.Sound('assets/Sounds/concrete-footsteps-6752.mp3')
        self.footstep_sound.set_volume(0.2)
        self.footstep_channel = pygame.mixer.Channel(1)
        self.shoot_channel = pygame.mixer.Channel(2)
        self.hitbox = Hitbox(self.position, self.hitbox_size)
        self.mag_size = 12
        self.mag_ammo = self.mag_size
        self.reserve_ammo = self.ammo - self.mag_size
        self.mag_ammo_bevore = self.mag_ammo
        self.ammo_bevore = self.ammo
        self.jump_strength = 1.5
        self.gun_spin_angle = 0
        self.gun_spin_speed = 720
        self.gun_spin_current = 0
        self.on_ground = False
        self.mode = False
        self.end = False
        self.decke_blockiert = False
        self.kann_springen = True

    def compute_cam_direction(self, gun, dt=1 / 60):
        """Berechnet die Kamerarichtung und aktualisiert die Waffe."""
        yaw_rad = np.radians(self.rx)
        pitch_rad = np.radians(self.ry)

        self.direction = np.array([
            np.cos(pitch_rad) * np.sin(yaw_rad),
            np.sin(pitch_rad),
            np.cos(pitch_rad) * np.cos(yaw_rad)
        ])
        self.direction = self.direction / np.linalg.norm(self.direction)

        self.right = np.cross(self.direction, self.up)
        self.right = self.right / np.linalg.norm(self.right)

        gun.rotation = [0, np.degrees(yaw_rad), 0]
        if hasattr(self, 'reload_gun_rotation'):
            del self.reload_gun_rotation
        gun.render()

    def god_mode(self):
        self.hitbox_cheat = self.mode
        self.flyhack = self.mode
        self.healhack = self.mode
        self.infinity = self.mode
        self.colider = not self.mode
        if self.mode:
            self.ammo_bevore = self.ammo
            self.mag_ammo_bevore = self.mag_ammo
            self.ammo = "∞"
            self.mag_ammo = "∞"
        else:
            self.ammo = self.ammo_bevore
            self.mag_ammo = self.mag_ammo_bevore

    def apply_transformations(self):
        """Wendet die Transformationen für die Spielerposition und -richtung an."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glRotatef(-self.ry, 1, 0, 0)
        glRotatef(-self.rx, 0, 1, 0)
        glTranslatef(-self.position[0], -self.position[1], -self.position[2])

    def handle_flying_movement(self, dt):
        """Verarbeitet die Flugbewegung des Spielers."""
        keys = pygame.key.get_pressed()

        if keys[K_LCTRL]:
            self.move_speed = 18
        else:
            self.move_speed = 10
        # Movement
        if keys[K_s]:
            self.position += self.direction * self.move_speed * dt
        if keys[K_w]:
            self.position -= self.direction * self.move_speed * dt
        if keys[K_d]:
            self.position -= self.right * self.move_speed * dt
        if keys[K_a]:
            self.position += self.right * self.move_speed * dt
        if keys[K_SPACE]:
            self.position += self.up * self.move_speed * dt
        if keys[K_LSHIFT]:
            self.position -= self.up * self.move_speed * dt

    def handle_events(self, enemies, dt):
        """Verarbeitet die Eingabeereignisse für den Spieler."""
        for e in pygame.event.get():
            if e.type == QUIT:
                sys.exit()
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                sys.exit()
            elif e.type == KEYDOWN and e.key == K_r:
                self.reload()
            elif e.type == MOUSEMOTION:
                self.dx, self.dy = e.rel
                self.rx -= self.dx
                self.ry = 0.000000000001
            elif e.type == MOUSEBUTTONDOWN and e.button == 1:
                if self.mag_ammo == "∞" or self.mag_ammo > 0:
                    self.raycast_shoot(enemies)
                else:
                    empty_sound = pygame.mixer.Sound('assets/Sounds/empty-gun-shot-6209.mp3')
                    empty_sound.set_volume(0.2)
                    self.shoot_channel.play(empty_sound)
            if e.type == KEYDOWN:
                if dt - self.last_input_time > 10000:
                    self.godmode_sequence = []

                self.last_input_time = dt
                self.godmode_sequence.append(pygame.key.name(e.key))

                # Trim to last 4 keys
                self.godmode_sequence = self.godmode_sequence[-4:]
                if self.godmode_sequence == self.godmode_code:
                    if self.mode:
                        self.mode = False
                    else:
                        self.mode = True
                    self.god_mode()
                    self.godmode_sequence = []

    def handle_movement(self, dt, hitboxes_map):
        """Verarbeitet die Bewegung des Spielers und die zugehörigen Sounds. Blockiert Bewegung bei Kollision mit Map-Hitboxen."""
        keys = pygame.key.get_pressed()

        move = np.array([0.0, 0.0, 0.0])
        if keys[K_w]:
            move -= self.direction
        if keys[K_s]:
            move += self.direction
        if keys[K_a]:
            move += self.right
        if keys[K_d]:
            move -= self.right
        move[1] = 0
        is_moving = np.linalg.norm(move) > 0
        if is_moving and self.on_ground:
            if not self.footstep_channel.get_busy():
                self.footstep_channel.play(self.footstep_sound, loops=-1)
        else:
            if self.footstep_channel.get_busy():
                self.footstep_channel.stop()
        if is_moving:
            move = move / np.linalg.norm(move)
        self.acceleration = move * self.move_speed

        self.velocity += self.acceleration * dt
        self.kann_springen = True
        self.decke_blockiert = False
        abstand = 0.1
        for i in range(1, 6):
            temp_position = self.position.copy()
            temp_position[1] += abstand * i
            temp_hitbox = Hitbox(temp_position, self.hitbox_size)
            for hitbox in hitboxes_map:
                if temp_hitbox.get_collision_vector(hitbox) is not None:
                    self.kann_springen = False
                    break
            if not self.kann_springen and self.velocity[1] >= 0:
                # Decke ist blockiert, wenn in irgendeinem Schritt eine Kollision erkannt wurde
                self.decke_blockiert = True
                break

        if self.on_ground:
            self.decke_blockiert = False
            self.kann_springen = True

        if keys[K_SPACE] and self.on_ground:
            if self.kann_springen:
                self.velocity[1] = max(self.velocity[1], 35) * self.jump_strength

        # Wenn die Decke blockiert ist, Y-Velocity auf 0 setzen und Player etwas nach unten schieben
        if self.decke_blockiert:
            self.velocity[1] = -1
            self.position[1] -= self.jump_strength * dt * 20  # Wert ggf. anpassen
        self.velocity *= self.friction
        velocity_norm = np.linalg.norm(self.velocity)
        if velocity_norm > self.max_speed:
            self.velocity = self.velocity / velocity_norm * self.max_speed

        # Neue Position berechnen und auf Kollision prüfen (x und z getrennt)
        new_position = self.position.copy()
        for axis in [0, 2]:  # 0 = x, 2 = z
            temp_position = new_position.copy()
            temp_position[axis] += self.velocity[axis] * dt
            temp_hitbox = Hitbox(temp_position, self.hitbox_size)
            temp_hitbox.position[1] += 1
            collision = False
            for hitbox in hitboxes_map:
                if temp_hitbox.get_collision_vector(hitbox) is not None:
                    collision = True
                    break
            if not collision:
                temp_hitbox.position[1] -= 1
                new_position[axis] = temp_position[axis]
            else:
                self.velocity[axis] = 0  # Stoppe Bewegung in diese Richtung
        self.position[0] = new_position[0]
        self.position[2] = new_position[2]

    def apply_gravity(self, hitboxes, dt):
        """Wendet die Schwerkraft auf den Spieler an und überprüft die Bodenkontakt. Gravity wird nicht angewendet, wenn die neue Position mit einer Hitbox kollidiert. hitboxes ist eine Liste von Hitboxen."""
        am_boden = False
        for hitbox in hitboxes:
            if self.hitbox.check_collision(hitbox, self):
                am_boden = True
                break
        if not self.flyhack:
            if am_boden:
                if self.velocity[1] < 0:
                    self.velocity[1] = 0
                self.on_ground = True
            else:
                # Vor dem Anwenden der Gravity prüfen, ob die neue Position kollidiert
                new_position = self.position.copy()
                new_position[1] += (self.velocity[1] - self.gravity * dt) * dt
                temp_hitbox = Hitbox(new_position, self.hitbox_size)
                collision = False
                for hitbox in hitboxes:
                    if temp_hitbox.get_collision_vector(hitbox) is not None:
                        collision = True
                        break
                if not collision:
                    self.velocity[1] -= self.gravity * dt
                self.on_ground = False
        self.position[1] += self.velocity[1] * dt
        if self.position[1] < 0:
            self.position[1] = 0
            self.velocity[1] = 0
            self.on_ground = True

    def check_collision(self, enemies, dt, pushback_multiplier=18):
        """Überprüft Kollisionen mit Map und Feinden und wendet ggf. Rückstoß an."""
        if self.mode:
            return False
        # Dann Feind-Kollisionen prüfen
        for enemy in enemies:
            if hasattr(enemy, "hitbox"):
                collision_vector_enemy = self.hitbox.get_collision_vector(enemy.hitbox)
                if collision_vector_enemy is not None:
                    collision_vector_enemy[1] = 0
                    self.position -= collision_vector_enemy * pushback_multiplier * dt
                    if not self.healhack:
                        self.hp -= enemy.damage
                    return True
            else:
                collision_vector_enemy = self.hitbox.get_collision_vector(enemy)
                if collision_vector_enemy is not None:
                    collision_vector_enemy[1] = 0
                    self.position -= collision_vector_enemy * pushback_multiplier * dt
                    return True
        return False

    def update_positions(self, gun):
        self.hitbox.position = self.position
        vor_offset = -2
        rechts_offset = -1.5
        unten_offset = -0.7
        gun.position = [
            self.position[0] + self.direction[0] * vor_offset + self.right[0] * rechts_offset + self.up[
                0] * unten_offset,
            self.position[1] + self.direction[1] * vor_offset + self.right[1] * rechts_offset + self.up[
                1] * unten_offset,
            self.position[2] + self.direction[2] * vor_offset + self.right[2] * rechts_offset + self.up[
                2] * unten_offset,
        ]

    def raycast_shoot(self, enemies):
        ray_origin = self.position
        if self.mag_ammo == "∞" or self.mag_ammo > 0:
            if not self.infinity:
                self.mag_ammo -= 1
            shoot_sound = pygame.mixer.Sound('assets/Sounds/pistol-shot.mp3')
            shoot_sound.set_volume(1.0)
            self.shoot_channel.play(shoot_sound)
            for enemy in enemies:
                if enemy.hitbox.check_ray_collision(ray_origin, -self.direction):
                    enemy.hp -= 1
                    return True
        return False

    def kill_if_dead(self, screen_width, screen_height, start_time):
        if self.hp <= 0 and not self.end:
            glClearColor(0.0, 0.0, 0.0, 1.0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            pygame.mixer.music.stop()
            self.end = True
            self.life_time = copy(pygame.time.get_ticks()) - start_time
        if self.end:
            life_font = pygame.font.Font('assets/StartMenu/Font/BLKCHCRY.TTF',
                                         int((150 // (screen_height * 0.00078125)) / 2))
            s = (self.life_time // 1000) % 60
            m = (s // 60) % 60
            h = m // 60
            life = life_font.render(f'Time you survived:', True,
                                    (132, 8, 0))
            life_time = life_font.render(f'{h:02}:{m:02}:{s:02}', True, (132, 8, 0))
            render_2D_texture(life, screen_width // 2 - ((life.get_width() // 2) * 2), screen_height // 2 - 100,
                              screen_width,
                              screen_height)
            render_2D_texture(life_time, screen_width // 2 // 2, screen_height // 2,
                              screen_width,
                              screen_height)
            pygame.display.flip()

    def reload(self):
        if not self.mag_ammo == "∞":
            nachzuladen = self.mag_size - self.mag_ammo
            nachgeladen = min(nachzuladen, self.ammo)
            if nachgeladen > 0:
                reload_sound = pygame.mixer.Sound('assets/Sounds/reload.mp3')
                reload_sound.set_volume(0.3)
                self.shoot_channel.play(reload_sound)
            self.mag_ammo += nachgeladen
            self.ammo -= nachgeladen
