import pygame
import math

from config_dataclass import *


class Bullet:
    def __init__(self, player, mouse_x, mouse_y):
        self.x = player.x + PlayerConfig().width / 2
        self.y = player.y + PlayerConfig().height / 2
        self.x_direction = mouse_x - self.x
        self.y_direction = mouse_y - self.y

        direction_lenght = math.sqrt(self.x_direction**2 + self.y_direction**2)
        if direction_lenght != 0:
            self.x_direction /= direction_lenght
            self.y_direction /= direction_lenght

    def update(self):
        self.x += self.x_direction * BulletConfig().speed
        self.y += self.y_direction * BulletConfig().speed

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            BulletConfig().color,
            (int(self.x), int(self.y)),
            BulletConfig().radius,
        )
