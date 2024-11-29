from player import Player
from bots import Bot, BotSprinter


class Simulation:
    def __init__(self):
        self.game_over = False
        self.draw_graphics = True
        self.player = Player()
        self.bullets = []

        self.bots: list[Bot] = []
        for _ in range(10):
            self.bots.append(Bot(self.player))
            self.bots.append(BotSprinter(self.player))

    def run(self):
        while not self.game_over:
            self.next_step()

    def next_step(self):
        pass
