class Player:
    def __init__(self):
        self.x = 0
        self.y = 0

    def move(self, dx, dy):
        self.x += dx
        self.y += dy


class Simulation:
    def __init__(self):
        self.game_over = False
        self.draw_graphics = True
        self.player = Player()

    def run(self):
        while not self.game_over:
            self.next_step()

    def next_step(self):
        pass
