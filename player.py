from config import PLAYER_START_X, PLAYER_START_Y


class Player:
    def __init__(self):
        self.x: int = PLAYER_START_X
        self.y: int = PLAYER_START_Y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
