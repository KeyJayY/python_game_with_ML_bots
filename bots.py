from turtle import down, up
import numpy as np
import pygame
from map import Map
from player import Player
from random import choice, randint
import math as mth
import heapq
import math
from icecream import ic

from config import BotConfig, MapConfig, SprinterBotConfig, PlayerConfig, WindowConfig


class Bot(Player):

    all_bots_positions = {"type": [], "x": [], "y": []}

    def __init__(self, player: Player, config: BotConfig = BotConfig()) -> None:
        super().__init__()
        self._player: Player = player
        self.type: str = "default"
        self.map = Map("map.json")

        self.config = config

        self.path = []
        self.target_index = 0
        self.last_player_position = (self._player.x, self._player.y)
        self.update_path_interval = 20
        self.frame_counter = 0
        self.grid = self.map.create_grid(self.config.cell_size)

        # Choosing where to spawn
        while True:
            self.x: float = randint(-WindowConfig().width, WindowConfig().width)
            self.y: float = randint(-WindowConfig().height, WindowConfig().height)
            self.spawn_distance_from_player: float = np.sqrt(
                (
                    self.x
                    + self.config.width / 2
                    - self._player.x
                    - self._player.width / 2
                )
                ** 2
                + (
                    self.y
                    + self.config.height / 2
                    - self._player.y
                    - self._player.height / 2
                )
                ** 2
            )
            if (
                self.config.max_spawn_radius
                >= self.spawn_distance_from_player
                >= self.config.min_spawn_radius
            ):
                break

    def _heuristic(self, a, b):
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

    def _is_valid_position_for_bot(self, position, all_bots_positions):
        """
        Checks if bot can be where it is - if it collides with obstacles or with other bots.
        """
        pos_y, pos_x = position

        # Sprawdzenie, czy wszystkie punkty zajmowane przez bota są wolne
        for dy in range(self.config.height):
            for dx in range(self.config.width):
                if not (
                    0 <= pos_y + dy < len(self.grid)
                    and 0 <= pos_x + dx < len(self.grid[0])
                ):
                    return False  # Poza granicami planszy
                if self.grid[pos_y + dy][pos_x + dx] == 1:  # 1 oznacza przeszkodę
                    return False  # Koliduje z przeszkodą

                # Sprawdzenie, czy pozycja jest zajęta przez inny bot
                for bot_position in all_bots_positions:
                    bot_y, bot_x = bot_position
                    for bot_dy in range(self.config.height):
                        for bot_dx in range(self.config.width):
                            if (pos_y + dy == bot_y + bot_dy) and (
                                pos_x + dx == bot_x + bot_dx
                            ):
                                return False  # Pozycja jest zajęta przez innego bota

        return True

    def spawn(self):
        x = randint(0, self.map.width - self.config.width)
        y = 0  # randint(0, self.map.height - self.config.height)

        # up = (x, 0)
        # down = (x, self.map.height-self.config.height)
        # left = (0, y)
        # right = (self.map.width-self.config.width, y)

        # new_x, new_y = choice([down, right])

        new_x, new_y = x, y

        self.x: float = new_x
        self.y: float = new_y

    def _debug_draw_line(self, screen: pygame.Surface):
        pygame.draw.line(
            screen, (255, 0, 0), (self.x, self.y), (self.target_x, self.target_y)
        )

    def _debug_draw_line_center(self, screen: pygame.Surface):
        pygame.draw.line(
            screen,
            (0, 255, 0),
            (self.x + self.config.width / 2, self.y + self.config.height / 2),
            (
                self.target_x + self.config.width / 2,
                self.target_y + self.config.height / 2,
            ),
        )

    def draw_bot(self, screen: pygame.Surface) -> None:
        # self._debug_draw_grid(screen,self.grid,self.path)
        pygame.draw.rect(
            screen,
            self.config.color,
            (
                self.x,
                self.y,
                self.config.width,
                self.config.height,
            ),
        )
        self._debug_draw_line(screen)
        self._debug_draw_line_center(screen)

    def die(self):
        self.spawn()

    def is_colliding(
        self,
        future_x: float,
        future_y: float,
    ) -> bool:
        """
        If new position is coliding with any obstacle on the map or with the player returns `True`.
        """
        bot_rect = pygame.Rect(
            future_x, future_y, self.config.width, self.config.height
        )

        # Collisions with obstacles
        if self.map.obstacles:
            for obstacle in self.map.obstacles:
                obstacle_rect = pygame.Rect(
                    obstacle["x"], obstacle["y"], obstacle["width"], obstacle["height"]
                )
                if bot_rect.colliderect(obstacle_rect):
                    return True

        # Collisions with player
        player_rect = pygame.Rect(
            self._player.x, self._player.y, self._player.width, self._player.height
        )
        if bot_rect.colliderect(player_rect):
            return True

        return False

    def move_to_player(self):
        self.target_x = self._player.x + self._player.width / 2 - self.config.width / 2
        self.target_y = (
            self._player.y + self._player.height / 2 - self.config.height / 2
        )


class BotSprinter(Bot):
    def __init__(self, player: Player) -> None:
        super().__init__(player, SprinterBotConfig())
        self.type: str = "sprinter"
        self.start_time = None
        self.current_speed = 0
        self.moving = True
