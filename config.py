import numpy as np

####################################################################
#############################  WINDOW  #############################
####################################################################
WINDOW_WIDTH: int = 600
WINDOW_HEIGHT: int = 600

####################################################################
##############################  GAME  ##############################
####################################################################
GAME_FPS: int = 60

####################################################################
#############################  COLORS  #############################
####################################################################
COLOR_BLACK: tuple[int, int, int] = 0, 0, 0
COLOR_RED: tuple[int, int, int] = 255, 0, 0
COLOR_GREEN: tuple[int, int, int] = 0, 255, 0
COLOR_BLUE: tuple[int, int, int] = 0, 0, 255
COLOR_ORANGE: tuple[int, int, int] = 255, 127, 0

############################  BACKGROUND  ############################
BG_COLOR: tuple[int, int, int] = COLOR_BLACK
OBSTACLE_COLOR: tuple[int, int, int] = COLOR_GREEN

####################################################################
#############################  PLAYER  #############################
####################################################################
PLAYER_COLOR: tuple[int, int, int] = COLOR_BLUE
PLAYER_WIDTH: int = 10
PLAYER_HEIGHT: int = 10
PLAYER_RADIUS: int = round(np.sqrt(PLAYER_WIDTH**2 + PLAYER_HEIGHT**2) / 2)

PLAYER_START_X: int = (WINDOW_WIDTH - PLAYER_WIDTH) // 2
PLAYER_START_Y: int = (WINDOW_HEIGHT - PLAYER_HEIGHT) // 2

PLAYER_SPEED: int = 2

####################################################################
#############################  BULLET  #############################
####################################################################
BULLET_COLOR: tuple[int, int, int] = 255, 255, 0

BULLET_SPEED: int = 10
BULLET_RADIUS: int = 1


####################################################################
##############################  BOTS  ##############################
####################################################################

############################  DEFAULT BOT  ############################
BOT_DEFAULT_COLOR: tuple[int, int, int] = COLOR_RED
BOT_DEFAULT_WIDTH: int = 10
BOT_DEFAULT_HEIGHT: int = 10
BOT_DEFAULT_RADIUS: int = round(
    np.sqrt(BOT_DEFAULT_WIDTH**2 + BOT_DEFAULT_HEIGHT**2) / 2
)

BOT_DEFAULT_SPEED: int = 1

BOT_DEFAULT_SPAWN_RANGE: int = 200  # R - r for ring
BOT_DEFAULT_SPAWN_RADIUS: int = PLAYER_RADIUS + BOT_DEFAULT_RADIUS + 100  # r for ring


MIN_DEFAULT_SPAWN_DISTANCE_FROM_PLAYER: int = BOT_DEFAULT_SPAWN_RADIUS
MAX_DEFAULT_SPAWN_DISTANCE_FROM_PLAYER: int = (
    MIN_DEFAULT_SPAWN_DISTANCE_FROM_PLAYER + BOT_DEFAULT_SPAWN_RANGE
)

############################  SPRINTER  ############################
BOT_SPRINTER_COLOR: tuple[int, int, int] = COLOR_ORANGE
BOT_SPRINTER_WIDTH: int = 5
BOT_SPRINTER_HEIGHT: int = 5
BOT_SPRINTER_RADIUS: int = round(
    np.sqrt(BOT_SPRINTER_WIDTH**2 + BOT_SPRINTER_HEIGHT**2) / 2
)

BOT_SPRINTER_SPEED: int = 3 * BOT_DEFAULT_SPEED

BOT_SPRINTER_SPAWN_RANGE: int = BOT_DEFAULT_SPAWN_RANGE  # R - r for ring
BOT_SPRINTER_SPAWN_RADIUS: int = PLAYER_RADIUS + BOT_SPRINTER_RADIUS + 100  # r for ring


MIN_SPRINTER_SPAWN_DISTANCE_FROM_PLAYER: int = BOT_SPRINTER_SPAWN_RADIUS
MAX_SPRINTER_SPAWN_DISTANCE_FROM_PLAYER: int = (
    MIN_SPRINTER_SPAWN_DISTANCE_FROM_PLAYER + BOT_SPRINTER_SPAWN_RANGE
)
