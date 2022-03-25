import pygame
import os
from .enemy import Enemy
from functions import *
imgs = []

for x in range(4):
    add_str = str(x)
    imgs.append(pygame.transform.scale(
        load_image("game_assets", "dragon_1_" + add_str + ".png"),
        (64, 64)))

death_sequence = []
for x in range(1, 6):
    death_sequence.append(pygame.transform.scale(load_image("game_assets", "dead_explode_" + str(x) + ".png"),
        (64, 64)))
pygame.init()
death_sound = pygame.mixer.Sound(os.path.join("game_assets", "dragon_death.wav"))

class Dragon(Enemy):
    def __init__(self):
        super().__init__()
        self.name = "Dragon"
        self.money = 50
        self.max_health = 45
        self.health = self.max_health
        self.gate_damage = 100
        self.imgs = imgs[:]
        self.speed_increase = 3.4
        self.size = 1.4
        self.boundary = (0.85 * self.speed_increase)
        self.death_sequence = death_sequence
        self.death_sound = death_sound
        #imgs[:]



