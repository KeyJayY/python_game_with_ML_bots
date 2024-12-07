import numpy as np
import pygame
from player import Player
from random import randint
import math as mth
from bullet import Bullet
import time

from config import BotConfig, SprinterBotConfig, PlayerConfig, WindowConfig


class Bot(Player):
    def __init__(self, player: Player) -> None:
        super().__init__()
        self._player: Player = player
        self.type: str = "default"

        # Choosing where to spawn
        while True:
            self.x: int = randint(-WindowConfig().width, WindowConfig().width)
            self.y: int = randint(-WindowConfig().height, WindowConfig().height)
            self.spawn_distance_from_player: float = np.sqrt(
                (
                    self.x
                    + BotConfig().height / 2
                    - self._player.x
                    - PlayerConfig().width / 2
                )
                ** 2
                + (
                    self.y
                    + BotConfig().height / 2
                    - self._player.y
                    - PlayerConfig().height / 2
                )
                ** 2
            )
            if (
                BotConfig().max_spawn_radius
                >= self.spawn_distance_from_player
                >= BotConfig().min_spawn_radius
            ):
                break

    def draw_bot(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(
            screen,
            BotConfig().color,
            (
                self.x,
                self.y,
                BotConfig().height,
                BotConfig().height,
            ),
        )

    def _get_vector_to_player_parameters(self, bot_width, bot_height) -> np.ndarray:
        vector_to_player: np.ndarray = np.array(
            [
                self.x + bot_width / 2 - (self._player.x + PlayerConfig().width / 2),
                self.y + bot_height / 2 - (self._player.y + PlayerConfig().height / 2),
            ]
        )
        return vector_to_player

    def move_to_player(self):
        vector: np.ndarray = self._get_vector_to_player_parameters(
            BotConfig().height, BotConfig().height
        )

        # Random movement, but most likely towards player
        angle = np.random.normal(0, 80)
        angle_rad = mth.radians(angle)

        dx, dy = vector
        cos_theta, sin_theta = mth.cos(angle_rad), mth.sin(angle_rad)
        rotated_vector = np.array(
            [
                dx * cos_theta - dy * sin_theta,
                dx * sin_theta + dy * cos_theta,
            ]
        )

        # Pseudo collisions
        if np.linalg.norm(rotated_vector) < PlayerConfig().radius + BotConfig().radius:
            return

        rotated_vector_normalized = rotated_vector / np.linalg.norm(rotated_vector)
        self.x -= rotated_vector_normalized[0] * BotConfig().speed
        self.y -= rotated_vector_normalized[1] * BotConfig().speed


class BotSprinter(Bot):
    def __init__(self, player: Player) -> None:
        super().__init__(player)
        self.type: str = "sprinter"
        self.start_time = None
        self.current_speed = 0
        self.moving = True

    def draw_bot(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(
            screen,
            SprinterBotConfig().color,
            (
                self.x,
                self.y,
                SprinterBotConfig().width,
                SprinterBotConfig().height,
            ),
        )

    def move_to_player(self):
        if self.start_time is None or not self.moving:
            self.start_time = pygame.time.get_ticks()
            self.moving = True
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000

        # Acceleration
        if elapsed_time < SprinterBotConfig().time_to_max_speed:
            self.current_speed = SprinterBotConfig().speed * (
                elapsed_time / SprinterBotConfig().time_to_max_speed
            )
        else:
            self.current_speed = SprinterBotConfig().speed

        vector: np.ndarray = self._get_vector_to_player_parameters(
            SprinterBotConfig().width, BotConfig().height
        )
        vector_normalized = vector / np.linalg.norm(vector)

        new_x = self.x - vector_normalized[0] * self.current_speed
        new_y = self.y - vector_normalized[1] * self.current_speed

        current_distance_to_player = np.sqrt(
            (
                new_x
                + SprinterBotConfig().width / 2
                - self._player.x
                - PlayerConfig().width / 2
            )
            ** 2
            + (
                new_y
                + SprinterBotConfig().height / 2
                - self._player.y
                - PlayerConfig().height / 2
            )
            ** 2
        )

        # Pseudo collisions
        if (
            current_distance_to_player
            < PlayerConfig().radius + SprinterBotConfig().radius
        ):
            self.moving = False
            return

        self.x = new_x
        self.y = new_y
