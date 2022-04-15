import pygame

from .item import Item
pygame.font.init()
popup_font = pygame.font.SysFont("segoeuisemilight", 14)

class Counter(Item):

    def __init__(self, text, x, y):
        self.x = x
        self.y = y
        self.start_y = y
        self.text = text
        self.despawn_timer = 50

    def draw(self, win):
        popt = popup_font.render("+" + str(self.text), 1, (245,245,220))
        win.blit(popt, (self.x - popt.get_width()/2, self.y))
        self.y -= 3
