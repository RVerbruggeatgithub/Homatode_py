import pygame
from menu.menu import *
import os
import math
from functions import *
from .item import Item
import random

item_image = pygame.transform.scale(load_image("game_assets", "gold.png"), (50, 50))


class Gold(Item):
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
        self.name = "gold"

    def draw(self, win):
        """
        draws the item
        :param win: surface
        :return: None
        """
        win.blit(self.img, (self.x - self.img.get_width()/2, self.y - self.img.get_height()/2))

    def pickup(self):
        """
        Generate random quantity of item
        :return: item quantity
        """
        return random.randint(self.min_quantity, self.max_quantity)