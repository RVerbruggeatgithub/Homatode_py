import pygame
import os
import math
from itertools import tee, islice, chain

def load_image(dir, path):
    return pygame.image.load(os.path.join(dir, path))


def get_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def point_direction(x1, y1, x2, y2, radians = False):
    if radians:
        return math.atan2((y2 - y1), (x2 - x1))
    else:
        return math.atan2((y2 - y1), (x2 - x1)) * 180 / math.pi


def previous_and_next(some_iterable):
    prevs, items, nexts = tee(some_iterable, 3)
    prevs = chain([None], prevs)
    nexts = chain(islice(nexts, 1, None), [None])
    return zip(prevs, items, nexts)

