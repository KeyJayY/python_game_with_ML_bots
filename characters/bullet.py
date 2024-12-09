import pygame
import math
import random

from config import BulletConfig, BotConfig, PlayerConfig
from map.obstacle import Obstacle
from characters.player import Player


class Bullet:

    def __init__(self, player: Player, direction, mode="single", type="player"):
        self.x = player.x + player.width / 2
        self.y = player.y + player.height / 2
        self.speed = BulletConfig().speed
        self.damage = BulletConfig().damage
        self.radius = BulletConfig().radius
        self.direction = direction

        self.mode = mode

        self.bot_width = BotConfig().width
        self.bot_height = BotConfig().height

        if mode == "shotgun":
            spread_angle = 0.2  # value in radians (1 radian = 57.2958 degrees)
            self.direction += random.uniform(-spread_angle, spread_angle)
            self.speed -= 4

        if type == "player":
            self.x = player.x + PlayerConfig().width / 2
            self.y = player.y + PlayerConfig().height / 2
        elif type == "bot1":
            self.x = player.x + BotConfig().width / 2
            self.y = player.y + BotConfig().height / 2

    def update(self):
        self.x += math.cos(self.direction) * self.speed
        self.y += math.sin(self.direction) * self.speed

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(
            screen,
            BulletConfig().color,
            (int(self.x), int(self.y)),
            BulletConfig().radius,
        )

    def check_bullet_collision_with_obstacles(self, obstacles: list[Obstacle]):
        bullet_left = self.x - self.radius
        bullet_right = self.x + self.radius
        bullet_top = self.y - self.radius
        bullet_bottom = self.y + self.radius

        for obstacle in obstacles:
            obstacle_left = obstacle.x
            obstacle_right = obstacle.x + obstacle.width
            obstacle_top = obstacle.y
            obstacle_bottom = obstacle.y + obstacle.height
            if not (
                bullet_right <= obstacle_left
                or bullet_left >= obstacle_right
                or bullet_bottom <= obstacle_top
                or bullet_top >= obstacle_bottom
            ):
                return True

        return False
