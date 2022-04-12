import pygame
from .tower import Tower
import os
import math
from menu.menu import *
from functions import *
import random

pygame.init()
bullet_hole = pygame.transform.scale(load_image("game_assets", "bullet_hole.png").convert_alpha(), (10, 10))
minigun_sound = pygame.mixer.Sound(os.path.join("game_assets", "minigun.mp3"))


# load tower images
turret_imgs = {}
for t in range (1, 4):
    turret_level_imgs = []
    for x in range(1, 4):
        turret_level_imgs.append(pygame.transform.scale(
            pygame.image.load(os.path.join("game_assets", "minigun_" +str(t) + "_" +str(x) + ".png")).convert_alpha(), (50, 50)))
    turret_imgs[t] = turret_level_imgs


class MinigunTower(Tower):
    def __init__(self, x,y):
        super().__init__(x, y)
        self.turret_image = turret_imgs[self.level][0]
        self.turret_imgs = turret_imgs
        self.tower_count = 0
        self.range = 150
        self.original_range = self.range
        self.inRange = False
        self.left = True
        self.damage = 2
        self.accuracy = 0.5
        self.original_damage = self.damage
        self.width = self.height = self.tower_base.get_width()
        self.moving = False
        self.name = "Minigun Tower"
        self.sell_value = [500,1000,2000]
        self.price = [1000,2000, "MAX"]
        self.upgrade_bonus_dmg = [0, 1, 3]
        self.upgrade_bonus_range = [0, 15, 25]
        self.upgrade_bonus_accuracy = [0, 0.05, 0.05]
        self.upgrade_bonus_atk_speed = [0, 4, 5]
        self.menu.set_tower_details(self)
        # attack speed, higher is faster. Anything above max_delay (tower()) will be set to 0 delay)
        self.attack_speed = 16
        # bullet hole image
        self.bullet_hole = bullet_hole
        # holes: [timer, x, y] remove when timer = 0
        self.holes = []
        self.action_sound = minigun_sound
        self.kill_locations = []

    def get_upgrade_cost(self):
        """
        gets the upgrade cost
        :return: int
        """
        return self.menu.get_item_cost()

    def draw(self, win):
        """
        draw the tower base and animated Minigun
        :param win: surface
        :return: int
        """
        super().draw_radius(win)
        super().draw(win)

        if self.inRange and not self.moving:
            self.tower_count += 1
            if self.tower_count >= len(self.turret_imgs[self.level]):
                self.tower_count = 0
        else:
            self.tower_count = 0

        if len(self.holes) > 0:
            for hole in self.holes:
                win.blit(self.bullet_hole, (hole[1], hole[2]))

        for kill_location in self.kill_locations:
            #([5, enemy.x, enemy.y, enemy.death_sequence])
            seq = kill_location[0]
            kill_x = kill_location[1] - 40
            kill_y = kill_location[2] - 40
            win.blit(kill_location[3][seq-1], (kill_x, kill_y))
            kill_location[0] -= 1
            if kill_location[0] < 0:
                self.kill_locations.remove(kill_location)

        # draw shadow
        surface = pygame.Surface((200, 200), pygame.SRCALPHA, 32)
        pygame.draw.circle(surface, (0, 0, 0, 94), (32, 40), 16, 0)
        win.blit(surface, (self.x - 32, self.y - 32))

        pivot_point = [self.x, self.y]
        offset = pygame.math.Vector2(-8, 0)
        turret_image, rect = self.rotate(self.turret_angle, offset, pivot_point)

        win.blit(turret_image, rect)
        if self.selected:
            self.menu.draw(win)

    def change_range(self, r):
        """
        change range of archer tower
        :param r: int
        :return: None
        """
        self.range = r

    def find_target(self, enemies):
        """
        attacks an enemy in the enemy list, modifies the list
        :param enemies: list of enemies
        :return: None
        """
        self.inRange = False
        enemy_closest = []
        for enemy in enemies:
            twr_center_x = self.x + self.turret_image.get_width() / 2 +20
            twr_center_y = self.y + self.turret_image.get_height() / 2 +20
            nme_center_x = enemy.x + enemy.img.get_width() / 2
            nme_center_y = enemy.y + enemy.img.get_height() / 2

            dis = math.sqrt((twr_center_x - nme_center_x)**2 + (twr_center_y - nme_center_y)**2)
            if dis < self.range:
                self.inRange = True
                enemy_closest.append(enemy)

        enemy_closest.sort(key=lambda x: x.path_pos)
        enemy_closest = enemy_closest[::-1]
        if len(enemy_closest) > 0:
            first_enemy = enemy_closest[0]
            y_mod = -1
            delta_y = first_enemy.y-self.y
            if 0 < delta_y > 0:
                y_mod = delta_y / abs(delta_y)
            self.turret_angle = point_direction(first_enemy.x, first_enemy.y, self.x, self.y)

            return self.attack(enemies, first_enemy)

            """
            if self.tower_count == 50:
                if first_enemy.hit(self.damage) == True:
                    money = first_enemy.money * 2
                    enemies.remove(first_enemy)
            """
        else:
            self.turret_image = self.turret_imgs[self.level][2]



    def attack(self, enemies, enemy):
        """
        rotate images here too?
        """
        #self.turret_image = turret_imgs[0]
        #self.turret_imgs = turret_imgs
        money = 0
        self.turret_image = turret_imgs[self.level][self.tower_count]
        # do bullets cycle here?
        if len(self.holes) > 0:
            for count, hole in enumerate(self.holes):
                hole[0] -= 1

                if hole[0] == 0:
                    self.holes.pop(count)

        self.delay -= self.attack_speed
        hit_chance = random.randint(1, 10) / 10
        if (self.delay <= 0):

            action_sound = pygame.mixer.Sound(self.action_sound)
            action_sound.set_volume(0.1)
            channel = pygame.mixer.find_channel(False)
            if not channel is None:
                channel.play(action_sound)
            dropping_items = []
            x_variety = random.randint(1, 20) - 10
            y_variety = random.randint(1, 20) - 10
            self.holes.append([5, enemy.x + x_variety, enemy.y + y_variety])
            if hit_chance >= self.accuracy:
                if enemy.hit(self.damage) == True:
                    self.holes = []
                    self.kill_locations.append([5, enemy.x, enemy.y, enemy.death_sequence])
                    dropping_items.append(enemy.items)
                    if channel:
                        channel.stop()
                    death_ = pygame.mixer.Sound(enemy.death_sound)
                    death_.set_volume(0.1)
                    death_.play()
                    enemies.remove(enemy)
                    return dropping_items
                    # add

            self.delay = self.max_delay


