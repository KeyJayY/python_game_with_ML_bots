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

        # Choosing where to spawn
        while True:
            self.x: int = randint(-WINDOW_WIDTH, WINDOW_WIDTH)
            self.y: int = randint(-WINDOW_HEIGHT, WINDOW_HEIGHT)
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

    def _get_vector_to_player_parameters(self, bot_width, bot_height) -> np.ndarray:
        vector_to_player: np.ndarray = np.array(
            [
                self.x + bot_width / 2 - (self._player.x + PLAYER_WIDTH / 2),
                self.y + bot_height / 2 - (self._player.y + PLAYER_HEIGHT / 2),
            ]
        )
        return vector_to_player

    def move_to_player(self):
        vector: np.ndarray = self._get_vector_to_player_parameters(
            BOT_DEFAULT_WIDTH, BOT_DEFAULT_HEIGHT
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
        if np.linalg.norm(rotated_vector) < PLAYER_RADIUS + BOT_DEFAULT_RADIUS:
            return

        rotated_vector_normalized = rotated_vector / np.linalg.norm(rotated_vector)
        self.x -= rotated_vector_normalized[0] * BOT_DEFAULT_SPEED
        self.y -= rotated_vector_normalized[1] * BOT_DEFAULT_SPEED


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
            BOT_SPRINTER_COLOR,
            (
                self.x,
                self.y,
                BOT_SPRINTER_WIDTH,
                BOT_SPRINTER_HEIGHT,
            ),
        )

    def move_to_player(self):
        if self.start_time is None or not self.moving:
            self.start_time = pygame.time.get_ticks()
            self.moving = True
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000

        # Acceleration
        if elapsed_time < BOT_SPRINTER_TIME_TO_MAX_SPEED:
            self.current_speed = BOT_SPRINTER_SPEED * (
                elapsed_time / BOT_SPRINTER_TIME_TO_MAX_SPEED
            )
        else:
            self.current_speed = BOT_SPRINTER_SPEED

        vector: np.ndarray = self._get_vector_to_player_parameters(
            BOT_SPRINTER_WIDTH, BOT_DEFAULT_HEIGHT
        )
        vector_normalized = vector / np.linalg.norm(vector)

        new_x = self.x - vector_normalized[0] * self.current_speed
        new_y = self.y - vector_normalized[1] * self.current_speed

        current_distance_to_player = np.sqrt(
            (new_x + BOT_SPRINTER_WIDTH / 2 - self._player.x - PLAYER_WIDTH / 2) ** 2
            + (new_y + BOT_SPRINTER_HEIGHT / 2 - self._player.y - PLAYER_HEIGHT / 2)
            ** 2
        )

        # Pseudo collisions
        if current_distance_to_player < PLAYER_RADIUS + BOT_SPRINTER_RADIUS:
            self.moving = False
            return

        self.x = new_x
        self.y = new_y
