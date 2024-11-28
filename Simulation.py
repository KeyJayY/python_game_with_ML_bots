from player import Player
from bots import Bot


class Simulation:
    def __init__(self):
        self.game_over = False
        self.draw_graphics = True
        self.player = Player()
        self.bullets = []

        self.bots: list[Bot] = []
        for _ in range(10000):
            self.bots.append(Bot(self.player))

    def run(self):
        while not self.game_over:
            self.next_step()

    def next_step(self):
        pass
