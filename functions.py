import pygame
import os
import math

def load_image(dir, path):
    return pygame.image.load(os.path.join(dir, path))

def get_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def point_direction(x1, y1, x2, y2, radians = False):
    if radians:
        return math.atan2((y2 - y1), (x2 - x1))
    else:
        return math.atan2((y2 - y1), (x2 - x1)) * 180 / math.pi

