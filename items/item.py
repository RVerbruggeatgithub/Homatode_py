import pygame
from menu.menu import *
import os
import math
from functions import *
import random

item_image = pygame.transform.scale(load_image("game_assets", "gold.png"), (50, 50))


class Item:
    """
    Abstract class for items
    When an enemy dies, an item will spawn at the location. Move mouse over it to pick it up.
    Currently only drop gold
    Future idea is to have components/materials that towers need to be build.
    """
    def __init__(self, x, y, min_q, max_q):
        self.x = x
        self.y = y
        self.min_quantity = min_q
        self.max_quantity = max_q
        self.img = item_image
        self.name = "item"

    def draw(self, win):
        """
        draws the item
        :param win: surface
        :return: None
        """

    def collide(self, x, y):
        """
        Detect collision with towers
        :param otherTower: list of polygon shapes
        :return: Bool
        """

        x1 = self.x
        y1 = self.y
        x2 = x
        y2 = y
        return self.collide_coordinates(x1, y1, x2, y2)

    def collide_coordinates(self, x1, y1, x2, y2):
        dis = math.sqrt((x2 - self.x)**2 + (y2 - self.y)**2)
        if dis >= self.img.get_width():
            return False
        else:
            return True

    def pickup(self):
        """
        Generate random quantity of item
        :return: item quantity
        """

    def update_location(self, x, y):
        self.x = x
        self.y = y
