from map import Map
from player import Player
from bots import Bot, BotSprinter

from config import PlayerConfig


class Simulation:
    def __init__(self):
        self.game_over = False
        self.draw_graphics = True
        self.player = Player()
        self.bullets = []
        self.map = Map()

        # Initializing bots
        self.bots: list[Bot] = []
        for _ in range(10):
            self.bots.append(Bot(self.player))
            self.bots.append(BotSprinter(self.player))

    def run(self):
        while not self.game_over:
            self.next_step()

    def check_collisions_with_obstacles(self):
        self.player.is_falling = True
        for obstacle in self.map.obstacles:
            if (
                self.player.x + self.player.width > obstacle.x
                and self.player.x < obstacle.x + obstacle.width
                and self.player.y + self.player.height <= obstacle.y
                and self.player.y + self.player.height + self.player.velocity_y
                >= obstacle.y
            ):
                self.player.y = obstacle.y - self.player.height
                self.player.velocity_y = 0
                self.player.is_falling = False

    def check_collisions(self):
        self.check_collisions_with_obstacles()

    def next_step(self):
        for bullet in self.bullets:
            bullet.update()
            if bullet.check_bullet_collision_with_obstacles(self.map.obstacles):
                self.bullets.remove(bullet)
        self.player.apply_y_movement()
        self.player.apply_gravity()
        self.check_collisions()
