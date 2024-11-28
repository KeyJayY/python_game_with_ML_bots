import pygame
import math

from config import *


class Bullet:
    def __init__(self, player, mouse_x, mouse_y):
        self.x = player.x + PLAYER_WIDTH / 2
        self.y = player.y + PLAYER_HEIGHT / 2
        self.bullet_speed = BULLET_SPEED
        self.radius = BULLET_RADIUS
        self.x_direction = mouse_x - self.x
        self.y_direction = mouse_y - self.y

        direction_lenght = math.sqrt(self.x_direction**2 + self.y_direction**2)
        if direction_lenght != 0:
            self.x_direction /= direction_lenght
            self.y_direction /= direction_lenght

    def update(self):
        self.x += self.x_direction * self.bullet_speed
        self.y += self.y_direction * self.bullet_speed

    def draw(self, screen):
        pygame.draw.circle(
            screen, BULLET_COLOR, (int(self.x), int(self.y)), self.radius
        )
