from player import Player
from bots import Bot
import json


class Map:
    def __init__(self, file_name):
        with open(file_name, "r") as file:
            data = json.load(file)
            self.width = data["width"]
            self.height = data["height"]
            self.obstacles = data["obstacles"]


class Simulation:
    def __init__(self):
        self.game_over = False
        self.draw_graphics = True
        self.player = Player()
        self.bullets = []
        self.map = Map("map.json")

        self.bots: list[Bot] = []
        # for _ in range(10000):
        #     self.bots.append(Bot(self.player))

    def run(self):
        while not self.game_over:
            self.next_step()

    def next_step(self):
        for bullet in self.bullets:
            bullet.update()
