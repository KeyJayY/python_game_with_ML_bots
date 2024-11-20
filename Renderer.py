import pygame
from Simulation import Simulation


class Renderer:
    def __init__(self, simulation):
        pygame.init()
        self.simulation = simulation
        self.screen = pygame.display.set_mode((400, 300))
        self.clock = pygame.time.Clock()

    def draw_frame(self):
        self.screen.fill((0, 0, 0))
        pygame.display.flip()

    def run(self):
        while not self.simulation.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.simulation.game_over = True
            self.draw_frame()
            self.simulation.next_step()
            self.clock.tick(60)
