import pygame
import os
from enemies.enemy import Enemy
from enemies.dragon import Dragon
from enemies.zombie import Zombie
from items.item import Item
from items.gold import Gold
from functions import *
#https://www.youtube.com/watch?v=iLHAKXQBOoA 2:06:00 towers!
from menu.menu import *
from towers.minigunTower import MinigunTower
from towers.rocketTower import RocketTower
import random
import time

play_btn = pygame.transform.scale(load_image("game_assets","button_play.png").convert_alpha(), (32, 32))
pause_btn = pygame.transform.scale(load_image("game_assets","button_pause.png").convert_alpha(), (32, 32))
tower_menu_img = pygame.transform.scale(load_image("game_assets","tower_menu.png").convert_alpha(), (120, 500))
menu_bg = pygame.transform.scale(load_image("game_assets","bottom_menu.png").convert_alpha(), (450, 250))
ico_minigun = pygame.transform.scale(load_image("game_assets","ico_minigun.png").convert_alpha(), (50, 50))
ico_rocket = pygame.transform.scale(load_image("game_assets","ico_rocket.png").convert_alpha(), (50, 50))
ico_laser = pygame.transform.scale(load_image("game_assets","ico_laser.png").convert_alpha(), (50, 50))
pygame.font.init()
attack_tower_names = ["Minigun Tower", "Rocket Tower"]
#for font in pygame.font.get_fonts():
#    print(font)

class Game:
    def __init__(self):
        self.width = 1500
        self.height = 800
        self.win = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.enemies = []
        self.gate_health = 1000
        self.money = 5000
        self.path = [(0, 429), (47, 429), (124, 418), (216, 386), (280, 353), (333, 329), (412, 323), (481, 276),
                     (540, 209), (600, 186), (656, 203), (718, 263), (820, 374), (900, 485), (916, 582), (953, 696),
                     (1008, 770), (1092, 780), (1180, 750), (1199, 661), (1222, 556), (1268, 518), (1292, 458),
                     (1285, 389), (1236, 338), (1209, 296), (1207, 220), (1216, 94), (1218, 18)]
        self.buildable_areas = [[(283, 393), (462, 360), (597, 240), (755, 378), (842, 564), (297, 582)],
                                [(108, 362), (302, 274), (435, 221), (532, 151), (664, 138), (848, 321), (922, 446),
                                 (967, 391), (1033, 249), (786, 9), (93, 13)],
                                [(1023, 793), (1497, 496), (1498, 797)]
                                ]
        self.gate_life_font = pygame.font.SysFont("comicsans", 32)
        self.bg = load_image("game_assets", "kremze.png")
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        self.gate = load_image("game_assets", "north_gate.png")
        self.gate = pygame.transform.scale(self.gate, (500, 300))
        self.gate = pygame.transform.rotate(self.gate, -50)
        self.gate_hp_indicator = pygame.transform.scale(load_image("game_assets", "gate_hp_indicator.png"), (32, 32))
        self.clicks = []
        self.timer = 0
        self.attack_towers = []
        self.pause = True
        self.moving_object = None
        self.play_pause_button = PlayPauseButton(play_btn, pause_btn, 129, self.height - 142)
        self.selected_tower = []
        self.items_list = [Gold(200, 200, 1, 10)]
        self.menu = buildingMenu(100, self.height - 25, 500, 200)
        self.menu.add_configured_btn(self.play_pause_button)
        minigun_t = MinigunTower(0, 0)
        rocket_t = RocketTower(0, 0)
        # below's second parameter is the name of the button
        self.menu.add_btn(ico_minigun, "buy_minigun", "Minigun", minigun_t.price[0])
        self.menu.add_btn(ico_rocket, "buy_rocket", "RocketTower",  rocket_t.price[0])
        self.menu.add_btn(ico_laser, "buy_chips", "Buy Chips",  minigun_t.price[0])
        self.menu.add_btn(ico_laser, "buy_cannon", "Buy Cannon", minigun_t.price[0])
        del minigun_t
        del rocket_t
        self.random_timer = 1

        #self.pause_btn = PlayPauseButton(sound_btn, sound_btn_off, 90, self.height - 85)

    def run(self):
        run = True
        clock = pygame.time.Clock()

        while run:

            if not self.pause:
                clock.tick(30)
                if time.time() - self.timer > random.randint(10, 40) / 15:
                        self.timer = time.time()
                        #self.random_timer = random.randint(10, 35) / 15
                        self.enemies.append(random.choice([Zombie(self.path)]))

            mouse_pos = pygame.mouse.get_pos()
            valid_area = False
            # Check for moving Objects:
            if self.moving_object:
                valid_area = self.moving_object.locations_collide(self.buildable_areas)
                self.moving_object.move(mouse_pos[0], mouse_pos[1])
                #tower_list = self.attack_towers[:] + self.support_towers[:]
                tower_list = self.attack_towers[:]
                collide = False
                if valid_area:
                    self.moving_object.place_color = (0, 0, 255, 100)
                else:
                    self.moving_object.place_color = (255, 0, 0, 100)

                for tower in tower_list:
                    if tower.collide(self.moving_object) and valid_area:
                        collide = True
                        tower.place_color = (255, 0, 0, 100)
                        self.moving_object.place_color = (255, 0, 0, 100)
                    else:
                        tower.place_color = (0, 0, 255, 100)
                        if not collide and not valid_area:
                            self.moving_object.place_color = (255, 0, 0, 100)

            # Event loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False


                for item in self.items_list:
                    if item.collide(mouse_pos[0], mouse_pos[1]):
                        if item.name == "gold":
                            self.money += item.pickup()
                        self.items_list.remove(item)

                if event.type == pygame.MOUSEBUTTONUP:
                    # if you're moving an object and click
                    if self.moving_object:

                        if event.button == 1:
                            allowed = True
                            hit = False
                            # tower_list = self.attack_towers[:] + self.support_towers[:]
                            # Bisection detection goes here...
                            """
                            1. get moving object coords.
                            2. Find closest two path coordinates
                            """

                            tower_list = self.attack_towers[:]

                            for tower in tower_list:
                                if tower.collide(self.moving_object):
                                    allowed = False

                            # if allowed and self.point_to_line(self.moving_object) and not hit:
                            if allowed and self.point_to_line(self.moving_object) and valid_area:

                                if self.moving_object.name in attack_tower_names:
                                    self.attack_towers.append(self.moving_object)
                                    self.money -= self.moving_object.price[0]
                                    self.moving_object.place_structure()
                                self.moving_object.moving = False
                                self.moving_object = None
                        elif event.button == 3:
                            self.moving_object = False
                        else:
                            continue
                    else:
                        # check for play or pause
                        if self.play_pause_button.click(mouse_pos[0], mouse_pos[1]):
                            self.pause = not (self.pause)
                            self.play_pause_button.paused = self.pause
                        """
                        if self.soundButton.click(pos[0], pos[1]):
                            self.music_on = not (self.music_on)
                            self.soundButton.paused = self.music_on
                            if self.music_on:
                                pygame.mixer.music.unpause()
                            else:
                                pygame.mixer.music.pause()
                        """
                        # look if you click on build menu
                        side_menu_button = self.menu.get_clicked(mouse_pos[0], mouse_pos[1])
                        print(self.menu.get_item_cost(side_menu_button), side_menu_button)
                        if side_menu_button:
                            cost = self.menu.get_item_cost(side_menu_button)
                            if self.money >= cost:
                                self.add_tower(side_menu_button)

                        # look if you clicked on attack tower
                        btn_clicked = None
                        if self.selected_tower:
                            btn_clicked = self.selected_tower.menu.get_clicked(mouse_pos[0], mouse_pos[1])
                            if btn_clicked:
                                if btn_clicked == "Upgrade":
                                    cost = self.selected_tower.get_upgrade_cost()
                                    if self.selected_tower.level < len(self.selected_tower.turret_imgs):
                                        if self.money >= cost:
                                            self.money -= cost
                                            self.selected_tower.upgrade()
                                if btn_clicked == "Sell":
                                    sales_value = self.selected_tower.get_sales_value()
                                    self.money += sales_value
                                    self.attack_towers.remove(self.selected_tower)

                        if not (btn_clicked):
                            for tw in self.attack_towers:
                                if tw.click(mouse_pos[0], mouse_pos[1]):
                                    tw.selected = True
                                    self.selected_tower = tw
                                else:
                                    tw.selected = False

                            # look if you clicked on support tower
                            """
                            for tw in self.support_towers:
                                if tw.click(mouse_pos[0], mouse_pos[1]):
                                    tw.selected = True
                                    self.selected_tower = tw
                                else:
                                    tw.selected = False
                            """
                """
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicks.append(mouse_pos)
                    print(self.clicks)
                """
            to_del = []
            if not self.pause:

                for enemy in self.enemies:
                    enemy.move()
                    if enemy.path_pos >= len(enemy.path) - 1:
                        to_del.append(enemy)

                for enemy in to_del:
                    self.gate_health -= enemy.gate_damage
                    # print(d.travelled_path)
                    self.enemies.remove(enemy)

                for tower in self.attack_towers:
                    # item dropping here..
                    result = tower.find_target(self.enemies)
                    if result is not None:
                        for items in result:
                            self.items_list = [*self.items_list, *items]

                # check for enemy HP here..
            """
                                # item dropping here..
                    result = tower.find_target(self.enemies)
                    if len(result) > 0:
                        # Join the lists
                        self.items_list = [*self.items_list, *result]
                        print(self.items_list)
            """

            if self.gate_health <= 0:
                print("You Lose")
                run = False
            self.draw()
        pygame.quit()

    def add_tower(self, name):
        x, y = pygame.mouse.get_pos()
        tower_opt_list = {"buy_minigun" : MinigunTower(x, y),
        "buy_rocket": RocketTower(x, y)}

        #if name == "buy_minigun":
        try:
                self.moving_object = tower_opt_list[name]
        except Exception as e:
            print(str(e) + "Invalid name")


    def sort_by_y(self, spr):
        """
        sort sprite by Y position
        :param spr: key comparison
        :returns: key value
        """
        return spr.y

    def point_to_line(self, tower):
        """
        returns if you can place tower based on distance from
        path
        :param tower: Tower
        :return: Bool
        """
        # find two closest points
        return True

    def draw_polygon_alpha(self, surface, color, points):
        lx, ly = zip(*points)
        min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
        target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
        shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        pygame.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in points])
        surface.blit(shape_surf, target_rect)

    def draw(self):
        #draw bg
        self.win.blit(self.bg, (0,0))

        if len(self.items_list) > 0:
            for item in self.items_list:
                item.draw(self.win)

        if self.moving_object:
            # , pygame.SRCALPHA, 32
            green_color = pygame.Color(75, 139, 59, 80)
            for buildable_area in self.buildable_areas:
                self.draw_polygon_alpha(self.win, green_color, buildable_area)
            # pygame.draw.polygon(self.win, green_color, self.buildable_areas, width=0)

            for tower in self.attack_towers:
                tower.draw_placement(self.win)

            #for tower in self.support_towers:
            #    tower.draw_placement(self.win)

            self.moving_object.draw_placement(self.win)
        """
        for p in self.clicks:
            pygame.draw.circle(self.win, (225,255,0), (p[0], p[1]), 5, 0)
        """

        if self.pause:
            # draw enemy travel path
            enemy = Enemy(self.path)
            # enemy.path
            """
            for section, node in enumerate(self.path):
                if (section +1) < len(self.path):
                    x1 = node[0]
                    y1 = node[1]
                    x2 = self.path[section+1][0]
                    y2 = self.path[section+1][1]
                    green_color = pygame.Color(75, 139, 59, 50)
                    pygame.draw.line(self.win, green_color, (x1, y1), (x2, y2), 25)
            """
        # draw gate
        self.win.blit(self.gate, (900, -280))
        # self.play_pause_button.draw(self.win)
        self.menu.draw(self.win)
        enemies = self.enemies
        for enemy in sorted(enemies, key=self.sort_by_y):
            enemy.draw(self.win)

        for tower in self.attack_towers:
            tower.draw(self.win)

        for tower in self.attack_towers:
            tower.draw_tower_menu(self.win)


        #lives
        text = self.gate_life_font.render(str(self.gate_health), 1, (0, 100, 0))
        money = self.gate_life_font.render(str(self.money), 1, (0, 100, 0))
        gate = self.gate_hp_indicator
        self.win.blit(gate, (0, 0))
        self.win.blit(text, (0, 32))
        self.win.blit(money, (0, 64))
        pygame.display.update()

g = Game()
g.run()