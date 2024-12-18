from map.map import Map
from characters.player import Player
from characters.bots import Bot, BotSprinter, PlayerLikeBot
import random
import math
from characters.bullet import Bullet
import characters.entity as ent

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
        self.entities.append(self.player.shoot(direction, "shotgun"))

    def next_step(self):
        for bot in self.player_like_bots:
            if random.randint(0, 10) == 1:
                self.entities.append(bot.random_shoot())

        for bot in self.bots:
            if random.randint(0, 10) == 1:
                self.entities.append(bot.random_shoot())

        self.update_entities()
        self.check_collisions()
        self.remove_queued_entities()

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
            elif isinstance(entity, Bot):
                entity.spawn()
                temp_ent.append(entity)
                entity.queued_for_deletion = False
            elif isinstance(entity, PlayerLikeBot):
                self.player_like_bots.remove(entity)
            elif entity is self.player:
                self.game_over = True
        self.entities.clear()
        self.entities = temp_ent
