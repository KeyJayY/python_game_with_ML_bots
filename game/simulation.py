from map.map import Map
from characters.player import Player
from characters.bots import Bot, BotSprinter, PlayerLikeBot
import random
import math
from characters.bullet import Bullet
import characters.entity as ent
import numpy as np

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
        self.entities: list[ent.Entity] = []

        self.entities.append(self.player)

        for obstacle in self.map.obstacles:
            self.entities.append(obstacle)

        for _ in range(2):
            bot = Bot(self.player)
            bot_sprinter = BotSprinter(self.player)
            player_like_bot = PlayerLikeBot()
            self.bots.append(bot)
            self.bots.append(bot_sprinter)
            self.player_like_bots.append(player_like_bot)
            self.entities.extend((bot, bot_sprinter, player_like_bot))

    def run(self):
        while not self.game_over:
            self.next_step()

    def bot_shoot(self):
        for bot in self.bots:
            if random.randint(0, 4) == 1 and type(bot) != BotSprinter:
                direction = math.atan2(
                    self.player.y - bot.y,
                    self.player.x - bot.x,
                )
                self.bullets.extend(bot.shoot(direction))

    def player_shoot(self, direction: float):
        self.entities.extend(self.player.shoot(direction))

    def check_if_win(self):
        if len(self.bots) == 0 and len(self.player_like_bots) == 0:
            self.game_over = True
            print("You win!")
        if self.player.health <= 0:
            self.game_over = True
            print(" You lose!")

    def next_step(self):
        for bot in self.player_like_bots:
            if random.randint(0, 10) == 1:
                self.entities.extend(bot.random_shoot())

        for bot in self.bots:
            if random.randint(0, 10) == 1:
                self.entities.extend(bot.random_shoot())

        self.update_entities()
        self.check_collisions()
        self.remove_queued_entities()
        for bot in self.bots:
            bot.weapon.update_countdown()
        self.player.weapon.update_countdown()
        for bot in self.player_like_bots:
            bot.weapon.update_countdown()
        self.check_if_win()

    def check_collisions(self):
        for entity1 in self.entities:
            for entity2 in self.entities:
                if entity1 != entity2 and entity1.check_collision(entity2):
                    entity1.evaluate_collision(entity2)

    def update_entities(self):
        for entity in self.entities:
            entity.update()

    def remove_queued_entities(self):
        temp_ent = []
        for entity in self.entities:
            entity.delete_if_too_far()
            if not entity.queued_for_deletion:
                temp_ent.append(entity)
            elif isinstance(entity, PlayerLikeBot):
                self.player_like_bots.remove(entity)
            elif isinstance(entity, Bot):
                self.bots.remove(entity)
        self.entities.clear()
        self.entities = temp_ent

    # get info functions for machine learning
    def get_enemies(self):
        data1 = [[bot.x, bot.y, bot.width, bot.height, bot.health] for bot in self.bots]
        data2 = [
            [bot.x, bot.y, bot.width, bot.height, bot.health]
            for bot in self.player_like_bots
        ]

        return np.array(data1 + data2, dtype=np.float32)

    def get_obstacles(self):
        return np.array(
            [
                [obstacle.x, obstacle.y, obstacle.width, obstacle.height]
                for obstacle in self.map.obstacles
            ],
            dtype=np.float32,
        )

    def get_actor(self):
        return {
            "position": np.array([self.player.x, self.player.y], dtype=np.float32),
            "health": self.player.health,
            "ammo": self.player.weapon.magazine,
            "isReloading": self.player.is_reloading(),
        }
