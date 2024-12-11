import pygame
from config import DefaultEntityConfig
from characters.bullet import Bullet


class Entity:
    def __init__(self):
        self.x = 20
        self.y = 20
        self.velocity_y: float = 0
        self.health = 100
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

    def rect(self):
        return [
            self,
        ]

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
