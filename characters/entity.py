import pygame
from config import DefaultEntityConfig
from characters.bullet import Bullet


class Entity:
    def __init__(self):
        self.x = DefaultEntityConfig().start_x
        self.y = DefaultEntityConfig().start_y
        self.velocity_y = 0
        self.health = DefaultEntityConfig().health
        self.width = DefaultEntityConfig().width
        self.height = DefaultEntityConfig().height
        self.config = DefaultEntityConfig()

    def draw(self, screen, offset_x=0, offset_y=0):
        pygame.draw.rect(
            screen,
            self.config.color,
            (
                self.x - offset_x,
                self.y - offset_y,
                self.width,
                self.height,
            ),
        )

    def reduce_health(self, damage: float):
        if self.health - damage < 0:
            self.health = 0
        else:
            self.health -= damage

    def shoot(self, direction, mode="single"):
        return Bullet(
            self,
            direction,
            mode,
        )
