import pygame
from config import DefaultEntityConfig, MapConfig

from enum import Enum, Flag
from config import DefaultEntityConfig

from config import Color
from config import HealthBarConfig


class CollisionLayers(Flag):
    NONE = 0
    GROUND = 1
    ACTOR = 2
    BULLET = 4
    WALL = 8


class CollisionInteractions(Flag):
    NOTHING = 0
    STAND = 1
    HURT = 2
    SACRIFICE = 4
    BLOCK = 8


class Entity:
    def __init__(self):
        self.x = DefaultEntityConfig().start_x
        self.y = DefaultEntityConfig().start_y
        self.velocity_y = 0
        self.health = DefaultEntityConfig().health
        self.width = DefaultEntityConfig().width
        self.height = DefaultEntityConfig().height
        self.config = DefaultEntityConfig()

        self.size = [self.width, self.height]

        self.collision_layer = CollisionLayers.NONE
        self.collision_interactions = {
            CollisionLayers.NONE: CollisionInteractions.NOTHING
        }
        self.queued_for_deletion: bool = False
        self.is_falling: bool = False
        self.damage = 0
        self.mass = 1
        self.last_frame_bullet_hit = False
        self.last_frame_bullet_kill = False
        self.get_hit_last_frame = False

    def draw(self, screen, offset_x=0, offset_y=0):
        pygame.draw.rect(
            screen,
            self.config.color,
            (
                self.x - self.width / 2 - offset_x,
                self.y - self.height / 2 - offset_y,
                self.width,
                self.height,
            ),
        )
        pygame.draw.rect(
            screen,
            Color().light_blue,
            (
                self.x - (HealthBarConfig().width) / 2 - offset_x,
                self.y - HealthBarConfig().y_offset - self.height / 2 - offset_y,
                self.health / 100 * HealthBarConfig().width,
                HealthBarConfig().height,
            ),
        )

    def reduce_health(self, damage: float):
        if self.health - damage <= 0:
            self.health = 0
            self.queued_for_deletion = True
        else:
            self.health -= damage

    def shoot(self, direction):
        return self.weapon.shoot(direction)

    def update(self):
        pass

    def check_collision(self, other):
        return (
            abs(self.x - other.x) <= self.width / 2 + other.width / 2
            and abs(self.y - other.y) <= self.height / 2 + other.height / 2
        )

    def evaluate_collision(self, other):
        other_layer = other.collision_layer
        if not other_layer in self.collision_interactions:
            return
        collision_response = self.collision_interactions[other_layer]

        if CollisionInteractions.STAND in collision_response:
            if (self.y - self.velocity_y) + self.size[1] / 2 <= other.y - other.size[
                1
            ] / 2:
                self.y = other.y - other.size[1] / 2 - self.size[1] / 2
                self.is_falling = False
                self.velocity_y = 0

        if CollisionInteractions.HURT in collision_response:
            if other.author != self:
                self.get_hit_last_frame = True
                other.author.last_frame_bullet_hit = True
                self.reduce_health(other.damage)
                if self.health <= 0:
                    other.author.last_frame_bullet_kill = True

        if CollisionInteractions.SACRIFICE in collision_response:
            if self.author != other:
                self.queued_for_deletion = True

        if CollisionInteractions.BLOCK in collision_response:
            pass

    def delete_if_too_far(self):
        tolerance = 0.1
        if (
            self.x < 0 - MapConfig().width * tolerance
            or self.y < 0 - MapConfig().height * tolerance
            or self.x > MapConfig().width * (1 + tolerance)
            or self.y > MapConfig().height * (1 + tolerance)
        ):
            self.queued_for_deletion = True
