import numpy as np
import pygame
from player import Player
from random import randint

from config import *


class Bot(Player):
    def __init__(self, player: Player) -> None:
        super().__init__()
        self._player = player
        self.type = "default"

        while True:
            self.x = randint(0, WINDOW_WIDTH)
            self.y = randint(0, WINDOW_HEIGHT)
            self.distance_from_player: float = np.sqrt(
                (self.x + BOT_DEFAULT_WIDTH / 2 - player.x - PLAYER_WIDTH / 2) ** 2
                + (self.y + BOT_DEFAULT_HEIGHT / 2 - player.y - PLAYER_HEIGHT / 2) ** 2
            )
            if (
                MAX_SPAWN_DISTANCE_FROM_PLAYER
                >= self.distance_from_player
                >= MIN_SPAWN_DISTANCE_FROM_PLAYER
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
