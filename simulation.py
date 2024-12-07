from player import Player
from bots import Bot, BotSprinter
import json
from bullet import Bullet

from config import PlayerConfig, BulletConfig


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
        self.map = Map("map2.json")
        self.bots_bullets=[]

        # Initializing bots
        self.bots: list[Bot] = []
        for _ in range(2):
            self.bots.append(Bot(self.player))
            self.bots.append(BotSprinter(self.player))

    def run(self):
        while not self.game_over:
            self.next_step()

    def check_collisions_with_obstacles(self):
        self.player.is_falling = True
        for obstacle in self.map.obstacles:
            if (
                self.player.x + PlayerConfig().width > obstacle["x"]
                and self.player.x < obstacle["x"] + obstacle["width"]
                and self.player.y + PlayerConfig().height <= obstacle["y"]
                and self.player.y + PlayerConfig().height + self.player.velocity_y
                >= obstacle["y"]
            ):
                self.player.y = obstacle["y"] - PlayerConfig().height
                self.player.velocity_y = 0
                self.player.is_falling = False

    def check_collisions(self):
        self.check_collisions_with_obstacles()

    def next_step(self):
        for bullet in self.bullets:
            bullet.update()
            if bullet.check_bullet_collision_with_obstacles(self.map.obstacles):
                self.bullets.remove(bullet)
            else:
                for bot in self.bots:
                    if bullet.check_bullet_collision_with_obstacles(bot.rect()):
                        bot.reduce_health(bullet.damage)
                        self.bullets.remove(bullet)
                        break
        for bullet in self.bots_bullets:
            bullet.update()
            if bullet.check_bullet_collision_with_obstacles(self.map.obstacles):
                self.bots_bullets.remove(bullet)
            elif(bullet.check_bullet_collision_with_obstacles(self.player.rect())):
                self.player.reduce_health(bullet.damage)
                self.bots_bullets.remove(bullet)
                if(len(self.bots)!=0 and bot.health==0):
                    self.bots.remove(bot)
        self.player.apply_y_movement()
        self.player.apply_gravity()
        self.check_collisions()
