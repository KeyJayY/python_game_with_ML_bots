from map.map import Map
from characters.player import Player
from characters.bots import Bot, BotSprinter, PlayerLikeBot
import random
import math
from characters.bullet import Bullet

from config import PlayerConfig


class Simulation:
    def __init__(self):
        self.game_over = False
        self.draw_graphics = True
        self.player = Player()
        self.bullets = []
        self.map = Map()
        self.bots_bullets = []

        # Initializing bots
        self.bots: list[Bot] = []
        self.player_like_bots: list[PlayerLikeBot] = []
        for _ in range(2):
            self.bots.append(Bot(self.player))
            self.bots.append(BotSprinter(self.player))
            self.player_like_bots.append(PlayerLikeBot())

    def run(self):
        while not self.game_over:
            self.next_step()

    def check_collisions_with_obstacles(self, player):
        player.is_falling = True
        for obstacle in self.map.obstacles:
            if (
                player.x + player.width > obstacle.x
                and player.x < obstacle.x + obstacle.width
                and player.y + player.height <= obstacle.y
                and player.y + player.height + player.velocity_y >= obstacle.y
            ):
                player.y = obstacle.y - player.height
                player.velocity_y = 0
                player.is_falling = False

    def apply_gravity(self):
        self.player.apply_y_movement()
        self.player.apply_gravity()
        self.check_collisions_with_obstacles(self.player)
        for bot in self.player_like_bots:
            bot.apply_y_movement()
            bot.apply_gravity()
            self.check_collisions_with_obstacles(bot)

    def bot_shoot(self):
        if random.randint(0, 4) == 1 and self.bots:
            direction = math.atan2(
                self.player.y - self.bots[0].y,
                self.player.x - self.bots[0].x,
            )
            self.bots_bullets.append(Bullet(self.bots[0], direction, "single", "bot1"))

    def player_shoot(self, direction):
        self.bullets.append(Bullet(self.player, direction, "shotgun"))

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
            elif bullet.check_bullet_collision_with_obstacles(self.player.rect()):
                self.player.reduce_health(bullet.damage)
                self.bots_bullets.remove(bullet)

        for bot in self.bots:
            bot.move_to_player()

        for bot in self.player_like_bots:
            bot.random_movement()
            if random.randint(0, 10) == 1:
                self.bots_bullets.append(bot.random_shoot())

        self.apply_gravity()
        self.bot_shoot()
