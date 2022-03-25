import pygame
import os
from functions import *
import pickle
pygame.font.init()
pygame.display.init()
pygame.display.set_mode((1500, 800))
star = pygame.transform.scale(load_image("game_assets", "star.png").convert_alpha(), (20,18))
star2 = pygame.transform.scale(load_image("game_assets", "rocket.png").convert_alpha(), (20,20))
ico_background_image = pygame.transform.scale(load_image("game_assets", "button_empty.png").convert_alpha(), (64,64))


class Button:
    """
    Button class for menu objects
    """
    def __init__(self, menu, img, name, x, y):
        self.name = name
        self.img = img
        self.menu = menu
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.x = x
        self.y = y

    def click(self, X, Y):
        """
        returns if the positon has collided with the menu
        :param X: int
        :param Y: int
        :return: bool
        """
        if X <= self.x + self.width and X >= self.x:
            if Y <= self.y + self.height and Y >= self.y:
                return True
        return False

    def draw(self, win):
        """
        draws the button image
        :param win: surface
        :return: None
        """
        win.blit(self.img, (self.x, self.y))

    def update(self):
        """
        updates button position
        :return: None
        """
        self.x = self.menu.x - 50
        self.y = self.menu.y - 110

class BuildMenuIcon(Button):
    def __init__(self, img, name, fullname, x, y, cost):
        self.img = img
        self.name = name
        self.fullname = fullname
        self.x = x
        self.y = y
        self.cost = cost
        self.buildmenu_icon_background_image = ico_background_image


    def draw(self, win):
        """
        draws the button image
        :param win: surface
        :return: None
        """

        """
        border_color = (0, 49, 83, 155)
        background_color = (44, 56, 99, 90)
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        surface.fill(background_color)

        rectangle = pygame.Rect(int(self.x - (self.width/2)), int(self.y-120), self.width, self.height)
        win.blit(surface, rectangle)
        pygame.draw.rect(win, border_color, rectangle, width=2, border_radius=6)

        tower_title = self.small_font.render(self.tower.name, 1, (255, 255, 255))
        win.blit(tower_title, (self.x - self.width/2 + 15, self.y - 110))
        """
        win.blit(self.buildmenu_icon_background_image, (self.x-5, self.y-8))
        small_font = pygame.font.SysFont("segoeuisemilight", 10)
        title = small_font.render(self.fullname, 1, (255, 255, 255))

        win.blit(self.img, (self.x, self.y))
        win.blit(title, (self.x + self.img.get_width()/2 - title.get_width()/2 + 2, self.y + self.img.get_height()/2 + 10))

    def click(self, X, Y):
        """
        returns if the positon has collided with the menu
        :param X: int
        :param Y: int
        :return: bool
        """
        if X <= self.x + self.img.get_width() and X >= self.x:
            if Y <= self.y + self.img.get_height() and Y >= self.y:
                return True

        return False

class PlayPauseButton(Button):
    def __init__(self, play_img, pause_img, x, y):
        self.img = play_img
        self.play = play_img
        self.pause = pause_img
        self.x = x
        self.y = y
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.paused = True
        self.cost = None
        self.name = None

    def draw(self, win):
        if self.paused:
            win.blit(self.play, (self.x, self.y))
        else:
            win.blit(self.pause, (self.x, self.y))


class VerticalButton(Button):
    """
    Button class for menu objects
    """
    def __init__(self, x, y, img, name, cost=None):
        self.name = name
        self.img = img
        self.x = x
        self.y = y
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.cost = cost

    def add_toggle_btn(self, imgs, name):
        """
        adds buttons to menu
        :param imgs: list of images to toggle through
        :param name: str
        :return: None
        """
        self.items += 1
        self.buttons.append(Button(self, img, name))



class Menu:
    """
    menu

    """
    def __init__(self, x, y, width, height, menu_bg, sell_value):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("segoeuisemilight", 25)
        self.small_font = pygame.font.SysFont("segoeuisemilight", 10)
        self.bg = menu_bg
        self.buttons = []
        self.items = 0

    def add_btn(self, img, name):
        """
        adds buttons to menu
        :param img: surface
        :param name: str
        :return: None
        """
        self.buttons.append(Button(self, img, name, self.x + (self.items * 32) + 50, self.y - self.height + 10))
        self.items += 1

    def add_configured_btn(self, configured_button):
        self.items += 1
        self.buttons.append(configured_button)

    def get_clicked(self, X, Y):
        """
        return the clicked item from the menu
        :param X: int
        :param Y: int
        :return: str
        """
        for btn in self.buttons:
            if btn.click(X,Y):
                return btn.name

        return None

    def update(self):
        """
        update menu and button location
        :return: None
        """
        for btn in self.buttons:
            btn.update()

    def draw(self, win):
        """
        draws btns and menu bg
        :param win: surface
        :return: None
        """
        win.blit(self.bg, (self.x - self.width/2, self.y-120))
        for item in self.buttons:
            item.draw(win)


class TowerMenu(Menu):
    """
    menu for holding items
    """
    def __init__(self, x, y, width, height, menu_bg, sell_value):
        super().__init__(x, y, width, height, menu_bg, sell_value)
        self.item_cost = 0
        self.tower = None
        self.item_sale_value = 0
        self.item_upgrade_cost = 0
        self.width = width
        self.height = height


    def set_tower_details(self, tower):
        self.tower = tower


    def get_items_upgrade(self):
        """
        gets sales value of tower
        :return: int
        """
        return self.tower[self.tower.level]

    def get_item_cost(self):
        """
        gets cost of upgrade to next level
        :return: int
        """
        return self.tower.price[self.tower.level - 1]

    def draw(self, win):
        """
        draws btns and menu bg
        :param win: surface
        :return: None
        """
        #self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        #win.blit(self.bg, (self.x - self.width/2, self.y-120))
        star_str = "⭐"

        border_color = (0, 49, 83, 155)
        background_color = (44, 56, 99, 90)
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        surface.fill(background_color)

        rectangle = pygame.Rect(int(self.x - (self.width/2)), int(self.y-120), self.width, self.height)
        win.blit(surface, rectangle)
        pygame.draw.rect(win, border_color, rectangle, width=2, border_radius=6)

        tower_title = self.small_font.render(self.tower.name, 1, (255, 255, 255))
        win.blit(tower_title, (self.x - self.width/2 + 15, self.y - 110))

        for i in range(self.tower.level):
            win.blit(star, (self.x - self.width/2 + (i * star.get_width() + 15), self.y - 93))
        for item in self.buttons:
            item.draw(win)
            tower = self.tower
            upgrade_string = "Upgrade: $"+ str(tower.price[tower.level - 1])
            if tower.price[tower.level - 1] == "MAX":
                upgrade_string = "(Upgrade: " + str(tower.price[tower.level - 1])
            #win.blit(star, (item.x + item.width + 5, item.y+12))
            text = self.small_font.render(upgrade_string + ", sell value: $" + str(tower.sell_value[tower.level - 1]) + ")", 1, (255,255,255))
            win.blit(text, (self.x - self.width/2 + 15, item.y + item.width + 4))
        tower_info = []
        tower_info.append(["Damage", tower.damage, tower.get_next_level_info(tower.upgrade_bonus_dmg)])
        tower_info.append(["Attack Speed", tower.attack_speed, tower.get_next_level_info(tower.upgrade_bonus_atk_speed)])
        tower_info.append(["Attack Range", tower.range, tower.get_next_level_info(tower.upgrade_bonus_range)])
        tower_info.append(["Accuracy", int(tower.accuracy*100)/100, tower.get_next_level_info(tower.upgrade_bonus_accuracy)])

        for idx, details in enumerate(tower_info):
            detail = self.small_font.render((str(details[0]) +":"+ str(details[1])+" ("+ str(details[2])+")"), 1, (255, 255, 255))
            win.blit(detail, (self.x - self.width / 2 + 15, item.y + 50 + 14*idx ))

class buildingMenu(Menu):
    """
    Vertical Menu for side bar of game
    """
    def __init__(self, x, y, width, height, img=None):
        self.buttons = []
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.items = 0
        self.bg = img
        self.font = pygame.font.SysFont("segoeuisemilight", 25)

    def add_btn(self, img, name, fullname, cost):
        """
        adds buttons to menu
        :param img: surface
        :param name: str
        :return: None
        """

        btn_x = self.x + (self.items)*68 - 40
        self.items += 1
        btn_y = self.y-60
        self.buttons.append(BuildMenuIcon(img, name, fullname, btn_x, btn_y, cost))

    def get_item_cost(self, name):
        """
        gets cost of item
        :param name: str
        :return: int
        """
        for btn in self.buttons:
            if btn.name == name:
                return btn.cost
        return -1

    def draw(self, win):
        """
        draws btns and menu bg
        :param win: surface
        :return: None
        """

        #win.blit(self.bg, (self.x - self.bg.get_width()/2, self.y-120))

        border_color = (0, 49, 83, 200)
        background_color = (44, 56, 99, 200)
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        surface.fill(background_color)

        rectangle = pygame.Rect(int(self.x), int(self.y-120), self.width, self.height)
        win.blit(surface, rectangle)
        pygame.draw.rect(win, border_color, rectangle, width=2, border_radius=6)

        for item in self.buttons:
            item.draw(win)
            # if item.cost is not None:
            #    win.blit(star2, (item.x+2, item.y + item.height))
            #    text = self.font.render(str(item.cost), 1, (255,255,255))
            #    win.blit(text, (item.x + item.width/2 - text.get_width()/2 + 7, item.y + item.height + 5))




