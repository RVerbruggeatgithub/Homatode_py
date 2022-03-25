import pygame
import math
import os
from functions import *





class Enemy:
    def __init__(self):
        self.width = 64
        self.height = 64
        self.animation_count = 0
        self.health = 1
        self.vel = 3
        self.path = [(0, 429),(47, 429), (124, 418), (216, 386), (280, 353), (333, 329), (412, 323), (481, 276), (540, 209), (600, 186), (656, 203), (718, 263), (820, 374), (900, 485), (916, 582), (953, 696), (1008, 770), (1092, 780), (1180, 750), (1199, 661), (1222, 556), (1268, 518), (1292, 458), (1285, 389), (1236, 338), (1209, 296), (1207, 220), (1216, 94), (1218, 18)]
        self.travelled_path = []
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.img = pygame.image.load(os.path.join("game_assets", "rocket.png")).convert_alpha()
        self.dis = 0
        self.path_pos = 0
        self.move_count = 0
        self.move_dis = 0
        self.imgs = []
        #self.flipped = False
        self.max_health = 0
        self.speed_increase = 1
        # upon survival it will do this much damage to the gate
        self.gate_damage = 1
        self.angle = 0
        self.anim_seq = 0
        self.size = 1
        # max allowed deviation from a node
        self.boundary = (0.85 * self.speed_increase)
        self.death_sequence = []

    def draw(self, win):
        """
        Draws the enemy with the given images
        :param win: surface
        :return: None
        """
        """
        for dot in self.path:
            pygame.draw.circle(win, (255,0,255), dot, 10, 0)
        """

        self.img = self.imgs[self.animation_count]

        shadow_radius = self.img.get_width() / 4

        surface = pygame.Surface((200, 200), pygame.SRCALPHA, 32)
        pygame.draw.circle(surface, (0, 0, 0, 94), (32, (32 + shadow_radius / 2)), shadow_radius, 0)
        win.blit(surface, (self.x - 32, self.y - 32))

        self.img = pygame.transform.rotate(self.img, (self.angle+90))
        self.img =pygame.transform.scale(self.img, (self.width * self.size, self.height * self.size))
        win.blit(self.img, (self.x - self.img.get_width()/2, self.y - self.img.get_height()/2))
        self.draw_health_bar(win)

    def draw_health_bar(self, win):
        """
        draw health bar above enemy
        :param win: surface
        :return: None
        """
        length = 50
        move_by = length / self.max_health
        health_bar = round(move_by * self.health)

        pygame.draw.rect(win, (255, 255, 255), (self.x - 31, self.y - 41, (length+2), 6), 0)
        pygame.draw.rect(win, (255,0,0), (self.x-30, self.y- 40, length, 4), 0)
        pygame.draw.rect(win, (0, 255, 0), (self.x-30, self.y - 40, health_bar, 4), 0)

    def collide(self, X, Y):
        """
        Returns if position has hit enemy
        :param x: int
        :param y: int
        :return: Bool
        """
        if X <= self.x + self.width and X >= self.x:
            if Y <= self.y + self.height and Y >= self.y:
                return True
        return False

    def move(self):
        """
        Move enemy
        :return: None
        """
        self.anim_seq += 1
        if (self.anim_seq > 5):
            self.animation_count += 1
            self.anim_seq = 0

        if self.animation_count >= len(self.imgs):
            self.animation_count = 0

        x1, y1 = self.path[self.path_pos]
        if self.path_pos + 1 >= len(self.path):
            return
        else:
            x2, y2 = self.path[self.path_pos + 1]
        x2, y2 = self.path[self.path_pos+1]

        delta_x = x2 - x1
        delta_y = y2 - y1
        distance = math.sqrt(delta_x**2 + delta_y**2)
        y_mod = -1
        if 0 < delta_y > 0:
            y_mod = delta_y / abs(delta_y)
        slope_angle = point_direction(x2, y2, x1, y1, False) * y_mod * 0.0174532925
        new_move_x = self.speed_increase * -math.cos(slope_angle)
        new_move_y = self.speed_increase * math.sin(slope_angle) * -1 * y_mod

        self.angle = point_direction(x1, y1, x2, y2, False) * -1
        self.x = self.x + new_move_x
        self.y = self.y + new_move_y

        enemy_distance_to_next_hop = math.sqrt((self.x - x2)**2 + (self.y - y2)**2)
        if (-self.boundary <= enemy_distance_to_next_hop <= self.boundary):
            self.travelled_path.append(enemy_distance_to_next_hop)
            self.path_pos += 1

    def hit(self, damage):
        """
        Returns if an enemy has died and removes one health
        each call
        :return: Bool
        """
        self.health -= damage
        if self.health <= 0:
            return True
        return False
