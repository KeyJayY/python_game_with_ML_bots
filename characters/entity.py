import pygame
from config import DefaultEntityConfig, MapConfig
#from characters.bullet import Bullet
from enum import Enum, Flag

class CollisionLayers(Flag):
    NONE = 0
    GROUND = 1
    PLAYER = 2
    BOT = 4
    BULLET = 8
    BULLET_BOT = 16
    WALL = 32

class CollisionInteractions(Flag):
    NOTHING = 0
    STAND = 1
    HURT = 2
    SACRIFICE = 4
    BLOCK = 8

class Entity:
    def __init__(self):
        self.x = DefaultEntityConfig().start_x
        self.y = DefaultEntityConfig().start_y
        self.velocity_y = 0
        self.health = DefaultEntityConfig().health
        self.width = DefaultEntityConfig().width
        self.height = DefaultEntityConfig().height
        self.config = DefaultEntityConfig()
        self.size = [self.width,self.height]

        self.collision_layer = CollisionLayers.NONE
        self.collision_interactions = {CollisionLayers.NONE:
                                       CollisionInteractions.NOTHING}
        self.queued_for_deletion: bool = False
        self.is_falling: bool = False
        self.damage = 0
        self.mass = 1



    def draw(self, screen, offset_x=0, offset_y=0):
        pygame.draw.rect(
            screen,
            self.config.color,
            (
                self.x - self.size[0]/2 - offset_x,
                self.y - self.size[1]/2 - offset_y,
                self.size[0],
                self.size[1],
            ),
        )

    def reduce_health(self, damage: float):
        if self.health - damage <= 0:
            self.health = 0
            self.queued_for_deletion = True
        else:
            self.health -= damage


    
    def shoot(self, direction, mode="single"):
        pass



    def update(self):
        pass
        
    def check_collision(self,other):
        return (abs(self.x-other.x) <= self.size[0]/2 + other.size[0]/2 and
            abs(self.y-other.y) <= self.size[1]/2 + other.size[1]/2)

    
    def evaluate_collision(self, other):
        other_layer = other.collision_layer
        if not other_layer in self.collision_interactions:
             return
        collision_response = self.collision_interactions[other_layer]
        
        if CollisionInteractions.STAND in collision_response:
            self.is_falling = False
            self.velocity_y = 0
            if (other.y - self.y -self.size[1]/2-other.size[1]/2 <0):
                push_force = 10
                self.y -= min(push_force,-(other.y - self.y  -self.size[1]/2-other.size[1]/2))

        
        if CollisionInteractions.HURT in collision_response:
            self.reduce_health(other.damage)

        if CollisionInteractions.SACRIFICE in collision_response:
            self.queued_for_deletion = True
            
        if CollisionInteractions.BLOCK in collision_response:
            pass

        
    def delete_if_too_far(self):
        tolerance = 0.1
        if (self.x < 0 - MapConfig().width*tolerance or
            self.y < 0 - MapConfig().height*tolerance or
            self.x >  MapConfig().width*(1+tolerance) or
            self.y >  MapConfig().height*(1+tolerance)):
            self.queued_for_deletion = True
            
                    
                    