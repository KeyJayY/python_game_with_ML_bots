import numpy as np
import pygame
from player import Player
from random import randint
import math as mth

from config import *


class Bot(Player):
    def __init__(self, player: Player) -> None:
        super().__init__()
        self._player: Player = player
        self.type: str = "default"

        while True:
            self.x: int = randint(0, WINDOW_WIDTH)
            self.y: int = randint(0, WINDOW_HEIGHT)
            self.spawn_distance_from_player: float = np.sqrt(
                (self.x + BOT_DEFAULT_WIDTH / 2 - self._player.x - PLAYER_WIDTH / 2)
                ** 2
                + (self.y + BOT_DEFAULT_HEIGHT / 2 - self._player.y - PLAYER_HEIGHT / 2)
                ** 2
            )
            if (
                MAX_DEFAULT_SPAWN_DISTANCE_FROM_PLAYER
                >= self.spawn_distance_from_player
                >= MIN_DEFAULT_SPAWN_DISTANCE_FROM_PLAYER
            ):
                break

    def draw_bot(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(
            screen,
            BOT_DEFAULT_COLOR,
            (
                self.x,
                self.y,
                BOT_DEFAULT_WIDTH,
                BOT_DEFAULT_HEIGHT,
            ),
        )

    def _get_vector_to_player_parameters(self) -> np.ndarray:
        vector_to_player: np.ndarray = np.array(
            [
                self.x + BOT_DEFAULT_WIDTH / 2 - self._player.x - PLAYER_WIDTH / 2,
                self.y + BOT_DEFAULT_HEIGHT / 2 - self._player.y - PLAYER_HEIGHT / 2,
            ]
        )
        return vector_to_player

    def move_to_player(self):
        vector: np.ndarray = self._get_vector_to_player_parameters()

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
        if np.linalg.norm(rotated_vector) < PLAYER_RADIUS + BOT_DEFAULT_RADIUS:
            return
        rotated_vector_normalized = rotated_vector / np.linalg.norm(rotated_vector)
        self.x -= rotated_vector_normalized[0] * BOT_DEFAULT_SPEED
        self.y -= rotated_vector_normalized[1] * BOT_DEFAULT_SPEED


class BotSprinter(Bot):
    def __init__(self, player: Player) -> None:
        super().__init__(player)
        self.type: str = "default"

    def draw_bot(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(
            screen,
            BOT_SPRINTER_COLOR,
            (
                self.x,
                self.y,
                BOT_SPRINTER_WIDTH,
                BOT_SPRINTER_HEIGHT,
            ),
        )

    def move_to_player(self):
        vector: np.ndarray = self._get_vector_to_player_parameters()
        vector_normalized = vector / np.linalg.norm(vector)

        if np.linalg.norm(vector) < PLAYER_RADIUS + BOT_DEFAULT_RADIUS:
            return

        self.x -= vector_normalized[0] * BOT_DEFAULT_SPEED
        self.y -= vector_normalized[1] * BOT_DEFAULT_SPEED
