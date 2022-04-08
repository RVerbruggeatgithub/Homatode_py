import pygame
import math
import os
from functions import *
from .projectile import Projectile

projectile_image = pygame.transform.scale(load_image("game_assets", "rocket.png"),(25, 15))

class Rocket(Projectile):
    """
    Abstract class for projectiles
    """
    def __init__(self, x, y, target_x, target_y, target):
        super().__init__(x, y, target_x, target_y, target)
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.width = 0
        self.height = 0
        self.speed_increase = 14
        self.boundary = 16
        self.img = projectile_image
        self.angle = 0
        self.max_splash_range = 100;

    def set_target(self, x, y):
        self.target_x = x
        self.target_y = y

    def draw(self, win):
        """
        draws the tower
        :param win: surface
        :return: None
        """
        pivot_point = [self.x, self.y]
        offset = pygame.math.Vector2(12, 7)
        projectile_img, rect = self.rotate(self.angle, offset, pivot_point)

        win.blit(projectile_img, (self.x-self.img.get_width()//2, self.y-self.img.get_height()//2))

    def move(self):
        """
         Move projectile
         :return: None

        self.anim_seq += 1
        if (self.anim_seq > 5):
            self.animation_count += 1
            self.anim_seq = 0

        if self.animation_count >= len(self.imgs):
            self.animation_count = 0
        """
        self.update()
        delta_x =  self.x - self.target.x
        delta_y = self.y - self.target.y
        distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
        y_mod = -1
        spin = 0
        if 0 < delta_y > 0:
            y_mod = delta_y / abs(delta_y)
            spin = 180
        slope_angle = point_direction(self.target.x, self.target.y, self.x, self.y, False) * y_mod * 0.0174532925
        new_move_x = self.speed_increase * -math.cos(slope_angle)
        new_move_y = self.speed_increase * math.sin(slope_angle) * -1 * y_mod

        self.angle = point_direction(self.x, self.y, self.target.x, self.target.y) + 180
        self.x = self.x + new_move_x
        self.y = self.y + new_move_y

        distance_to_enemy = math.sqrt((self.x - self.target_x) ** 2 + (self.y - self.target_y) ** 2)
        if -self.boundary <= distance_to_enemy <= self.boundary:
            return False

        return True

    def rotate(self, angle, offset, pivot_point):
        """
        Rotate the surface around the pivot point.
        Args:
            angle (float): Rotate by this angle.
            pivot (tuple, list, pygame.math.Vector2): The pivot point.
            offset (pygame.math.Vector2): This vector is added to the pivot.
        """
        rotated_image = pygame.transform.rotozoom(self.img, (angle - 180)*-1, 1)  # Rotate the image.
        rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
        # Add the offset vector to the center/pivot point to shift the rect.
        rect = rotated_image.get_rect(center=pivot_point + rotated_offset)
        return rotated_image, rect  # Return the rotated image