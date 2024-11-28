import json


class Player:
    def __init__(self):
        self.x = 0
        self.y = 0

    def move(self, dx, dy):
        self.x += dx
        self.y += dy


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

    def run(self):
        while not self.game_over:
            self.next_step()

    def next_step(self):
        for bullet in self.bullets:
            bullet.update()
