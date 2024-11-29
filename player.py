from config_dataclass import *

class Player:
    def __init__(self):
        self.x: int = PlayerConfig().start_x
        self.y: int = PlayerConfig().start_y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
