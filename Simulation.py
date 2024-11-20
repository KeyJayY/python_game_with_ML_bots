class Simulation:
    def __init__(self):
        self.game_over = False
        self.draw_graphics = True

    def run(self):
        while not self.game_over:
            self.next_step()

    def next_step(self):
        print("a")
