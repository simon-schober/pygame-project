"""
Player-Modul
============

Dieses Modul enthält die Player-Klasse für das Spiel.
"""

import sys

import numpy as np
import pygame
from OpenGL.GL import *
from pygame import *

from Hitbox import Hitbox


def clamp(x, minimum, maximum):
    """Begrenzt x auf den Bereich [minimum, maximum]."""
    return max(minimum, min(x, maximum))


class Player:
    def __init__(self, position=None, rx=0, ry=0, move_speed=50, gravity=20,
                 direction=None, up=None, hitbox_size=None, hp=200.0, ammo=100,
                 velocity=None, acceleration=None, friction=0.8, max_speed=500.0):
        # Standardwerte für numpy-Arrays
        self.position = np.array([0.0, 10.0, 0.0]) if position is None else position
        self.direction = np.array([1.0, 0.0, 0.0]) if direction is None else direction
        self.up = np.array([0.0, 1.0, 0.0]) if up is None else up
        self.hitbox_size = np.array([2.0, 4.0, 2.0]) if hitbox_size is None else hitbox_size
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
        self.jump_strength = 1.0
        self.gun_spin_angle = 0
        self.gun_spin_speed = 720
        self.gun_spin_current = 0
        self.on_ground = False

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
            self.hitbox_cheat = True
            self.flyhack = True
            self.healhack = True
            self.infinity = True
            self.colider = True

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
                self.ry = clamp(self.ry - self.dy, -90, 90)
            elif e.type == MOUSEBUTTONDOWN and e.button == 1:
                if self.mag_ammo > 0:
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
                    self.god_mode()
                    self.godmode_sequence = []


    def handle_movement(self, dt):
        """Verarbeitet die Bewegung des Spielers und die zugehörigen Sounds."""
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
        # Nur horizontale Bewegung erlauben (Y ignorieren)
        move[1] = 0
        is_moving = np.linalg.norm(move) > 0
        # Sound nur abspielen, wenn man am Boden ist und sich bewegt
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
        # SPRINGEN MIT LEERTASTE
        if keys[K_SPACE] and self.on_ground:
            self.velocity[1] = 25.0  # Sprungkraft, ggf. als Attribut setzen
            self.on_ground = False
        self.velocity *= self.friction
        velocity_norm = np.linalg.norm(self.velocity)
        if velocity_norm > self.max_speed:
            self.velocity = self.velocity / velocity_norm * self.max_speed
        self.position[0] += self.velocity[0] * dt
        self.position[2] += self.velocity[2] * dt
        # self.position[1] bleibt unverändert

    def apply_gravity(self, objects, dt):
        """Wendet die Schwerkraft auf den Spieler an und überprüft die Bodenkontakt."""
        am_boden = False
        for obj in objects:
            if self.hitbox.check_collision(obj.hitbox, self):
                am_boden = True
                break
        if not self.flyhack:
            if am_boden:
                if self.velocity[1] < 0:
                    self.velocity[1] = 0
                self.on_ground = True
            else:
                self.velocity[1] -= self.gravity * dt
                self.on_ground = False
        self.position[1] += self.velocity[1] * dt
        # Optional: Bodenhöhe (z.B. y=0) erzwingen
        if self.position[1] < 0:
            self.position[1] = 0
            self.velocity[1] = 0
            self.on_ground = True

    def check_collision(self, enemies, dt, pushback_multiplier=18):
        """Überprüft Kollisionen mit Feinden und wendet ggf. Rückstoß an."""
        for enemy in enemies:
            collision_vector = self.hitbox.get_collision_vector(enemy.hitbox)
            if collision_vector is not None:
                self.position -= collision_vector * pushback_multiplier * dt  # Spieler wird im Kollisionsvektor zurückgeschoben
                if not self.healhack:
                    self.hp -= enemy.damage
                return True
        return False

    def update_positions(self, gun):
        self.hitbox.position = self.position
        gun.position = [self.position[0], self.position[1] - 1.25, self.position[2]]

    def raycast_shoot(self, enemies):
        ray_origin = self.position
        if self.mag_ammo > 0:
            if not self.infinity:
                self.mag_ammo -= 1
            shoot_sound = pygame.mixer.Sound('assets/Sounds/pistol-shot.mp3')
            shoot_sound.set_volume(0.2)
            self.shoot_channel.play(shoot_sound)
            for enemy in enemies:
                if enemy.hitbox.check_ray_collision(ray_origin, -self.direction):
                    enemy.hp -= 1
                    return True
        return False

    def kill_if_dead(self):
        if not self.hp:
            sys.exit()

    def reload(self):
        nachzuladen = self.mag_size - self.mag_ammo
        nachgeladen = min(nachzuladen, self.ammo)
        if nachgeladen > 0:
            reload_sound = pygame.mixer.Sound('assets/Sounds/reload.mp3')
            reload_sound.set_volume(0.3)
            self.shoot_channel.play(reload_sound)
        self.mag_ammo += nachgeladen
        self.ammo -= nachgeladen
