import numpy as np
from traitlets import Int

# Window properties
WINDOW_WIDTH: int = 600
WINDOW_HEIGHT: int = 600

# Game properties
GAME_FPS: int = 60

# Color properties
COLOR_BLACK: tuple[int, int, int] = 0, 0, 0
COLOR_RED: tuple[int, int, int] = 255, 0, 0
COLOR_GREEN: tuple[int, int, int] = 0, 255, 0
COLOR_BLUE: tuple[int, int, int] = 0, 0, 255

# Colors
BG_COLOR: tuple[int, int, int] = COLOR_BLACK

# Player properties
PLAYER_COLOR: tuple[int, int, int] = COLOR_BLUE
PLAYER_WIDTH: int = 40
PLAYER_HEIGHT: int = 40
PLAYER_RADIUS: int = round(np.sqrt(PLAYER_WIDTH**2 + PLAYER_HEIGHT**2) / 2)

PLAYER_START_X: int = (WINDOW_WIDTH - PLAYER_WIDTH) // 2
PLAYER_START_Y: int = (WINDOW_HEIGHT - PLAYER_HEIGHT) // 2

PLAYER_SPEED: int = 5

# Bullet properties
BULLET_COLOR: tuple[int, int, int] = 255, 255, 0

BULLET_SPEED: int = 10
BULLET_RADIUS: int = 3

# Bot properties
BOT_DEFAULT_COLOR: tuple[int, int, int] = COLOR_RED
BOT_DEFAULT_WIDTH: int = 10
BOT_DEFAULT_HEIGHT: int = 10
BOT_DEFAULT_RADIUS: int = round(
    np.sqrt(BOT_DEFAULT_WIDTH**2 + BOT_DEFAULT_HEIGHT**2) / 2
)

BOT_DEFAULT_SPEED: int = 1

BOT_DEFAULT_SPAWN_RANGE: int = 200  # R - r for ring
BOT_DEFAULT_SPAWN_RADIUS: int = PLAYER_RADIUS + BOT_DEFAULT_RADIUS + 100  # r for ring


MIN_SPAWN_DISTANCE_FROM_PLAYER: int = BOT_DEFAULT_SPAWN_RADIUS
MAX_SPAWN_DISTANCE_FROM_PLAYER: int = (
    MIN_SPAWN_DISTANCE_FROM_PLAYER + BOT_DEFAULT_SPAWN_RANGE
)
