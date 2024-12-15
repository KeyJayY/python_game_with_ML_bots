from map.map import Map
from characters.player import Player
from characters.bots import Bot, BotSprinter, PlayerLikeBot
import random
import math
from characters.bullet import Bullet

from config import MapConfig


class Simulation:
    def __init__(self):
        self.game_over = False
        self.draw_graphics = True
        self.player: Player = Player()
        self.bullets: list[Bullet] = []
        self.map: Map = Map()

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

    def check_collisions_with_obstacles(self, entity):
        entity.is_falling = True
        for obstacle in self.map.obstacles:
            if (
                entity.x + entity.width > obstacle.x
                and entity.x < obstacle.x + obstacle.width
                and entity.y + entity.height <= obstacle.y
                and entity.y + entity.height + entity.velocity_y >= obstacle.y
            ):
                entity.y = obstacle.y - entity.height
                entity.velocity_y = 0
                entity.is_falling = False

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
            self.bullets.extend(self.bots[0].shoot(direction))

    def player_shoot(self, direction: float):
        self.bullets.extend(self.player.shoot(direction, "shotgun"))

    def update_weapon_countdowns(self):
        self.player.weapon.update_countdown()
        for bot in self.bots:
            bot.weapon.update_countdown()
        for bot in self.player_like_bots:
            bot.weapon.update_countdown()

    def remove_dead_bots(self):
        for bot in self.bots:
            if bot.health <= 0:
                self.bots.remove(bot)
        for bot in self.player_like_bots:
            if bot.health <= 0:
                self.player_like_bots.remove(bot)

    def check_game_over(self):
        if self.player.health <= 0:
            self.game_over = True
            print("loose")
        if not self.bots and not self.player_like_bots:
            self.game_over = True
            print("win")

    def check_bullet_colisions(self, bullet):
        if (
            bullet.x < 0
            or bullet.x > MapConfig().width
            or bullet.y < 0
            or bullet.y > MapConfig().height
        ):
            self.bullets.remove(bullet)
            return

        for obstacle in self.map.obstacles:
            if bullet.check_bullet_collision_with_object(obstacle):
                self.bullets.remove(bullet)
                return
        for bot in self.bots:
            if bullet.check_bullet_collision_with_object(bot):
                bot.reduce_health(bullet.damage)
                self.bullets.remove(bullet)
                return
        for bot in self.player_like_bots:
            if bullet.check_bullet_collision_with_object(bot):
                bot.reduce_health(bullet.damage)
                self.bullets.remove(bullet)
        if bullet.check_bullet_collision_with_object(self.player):
            self.player.reduce_health(bullet.damage)
            self.bullets.remove(bullet)
            return

    def next_step(self):
        for bullet in self.bullets:
            bullet.update()
            self.check_bullet_colisions(bullet)

        for bot in self.bots:
            bot.move_to_player()

        for bot in self.player_like_bots:
            bot.random_movement()
            if random.randint(0, 10) == 1:
                self.bullets.extend(bot.random_shoot())

        self.update_weapon_countdowns()
        self.apply_gravity()
        self.bot_shoot()
        self.remove_dead_bots()
        self.check_game_over()

    def reset(self):
        self.player.reset()
        for bot in self.bots:
            bot.reset()
        self.game_over = False
