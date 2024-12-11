from player import Player
import floor
from bots import Bot, BotSprinter
import json
from bullet import Bullet
from entity import Entity

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
        self.entities: list[Entity] = []
        
        for obstacle in self.map.obstacles:
            self.entities.append(floor.Platform(obstacle))

        # Initializing bots
        self.bots: list[Bot] = []
        for _ in range(2):
            self.bots.append(Bot(self.player))
            self.bots.append(BotSprinter(self.player))
            
        
        self.entities.append(self.player)
        
        for bot in self.bots:
            self.entities.append(bot)

    def run(self):
        while not self.game_over:
            self.next_step()

    def remove_queued_entities(self):
        temp_ent = []
        for entity in self.entities:
            entity.delete_if_too_far()
            if (not entity.queued_for_deletion):
                temp_ent.append(entity)
            elif isinstance(entity,Bot):
                self.bots.remove(entity)
            elif entity is self.player:
                self.game_over = True
        self.entities.clear()
        self.entities = temp_ent
        
    
    def update_entities(self):
        for entity in self.entities:
            entity.update()
            
    def chceck_collisions(self):
        for entity1 in self.entities:
            for entity2 in self.entities:
                if (entity1 != entity2 and
                    entity1.check_collision(entity2)):
                    entity1.evaluate_collision(entity2)

    def next_step(self):
        self.remove_queued_entities()
        self.update_entities()
        self.chceck_collisions()
    
