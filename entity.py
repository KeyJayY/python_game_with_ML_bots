import pygame
from math import sqrt
from enum import Enum, Flag
from config import WindowConfig

class Collision_layers(Flag):
    NONE = 0
    GROUND = 1
    PLAYER = 2
    BOT = 4
    BULLET = 8
    BULLET_BOT = 16
    WALL = 32

class Collision_interactions(Flag):
    NOTHING = 0
    STAND = 1
    HURT = 2
    SACRIFICE = 4
    BLOCK = 8


class Entity:
    def __init__(self):
        self.size = [0,0]
        self.shape: str = "rectangle"
        self.color: tuple[int] = [0,0,0]
        self.x = 0
        self.y = 0
        self.velocity_y: float = 0
        self.health = 100
        self.collision_layer = Collision_layers.NONE
        self.collision_interactions = {Collision_layers.NONE:
                                       Collision_interactions.NOTHING}
        self.queued_for_deletion: bool = False
        self.is_falling: bool = False
        self.damage = 0

    def draw(self, screen):
        if self.shape == "circle":
            pygame.draw.circle(
                screen,
                self.color,
                (int(self.x), int(self.y)),
                int(self.size[0]/2),
                )
        elif self.shape == "rectangle":
            pygame.draw.rect(
                screen,
                self.color,
                (
                    self.x - self.size[0]/2,
                    self.y - self.size[1]/2,
                    self.size[0],
                    self.size[1],
                ),
            )
        else:
            Warning("Unkown shape: {} not drawn".format(self.shape))
                
    def update(self):
        pass
        
    def check_collision(self,other):
        if self.shape == other.shape == "circle":
            return sqrt((self.x-other.x)**2+(self.y-other.y)**2) <= self.size[0]/2 + other.size[0]/2
        else:
            return (abs(self.x-other.x) <= self.size[0]/2 + other.size[0]/2 and
                abs(self.y-other.y) <= self.size[1]/2 + other.size[1]/2)

    
    def evaluate_collision(self, other):
        other_layer = other.collision_layer
        if not other_layer in self.collision_interactions:
             return
        collision_response = self.collision_interactions[other_layer]
        
        if Collision_interactions.STAND in collision_response:
            self.is_falling = False
            if (other.y - self.y -self.size[1]/2-other.size[1]/2 <0):
                push_force = 10
                self.y -= min(push_force,-(other.y - self.y -self.size[1]/2-other.size[1]/2))
                self.velocity_y = 0
                    
        
        if Collision_interactions.HURT in collision_response:
            self.health -= other.damage
            if self.health <=0:
                self.health = 0
                self.queued_for_deletion = True

        if Collision_interactions.SACRIFICE in collision_response:
            self.queued_for_deletion = True
            
            
    def delete_if_too_far(self):
        tolerance = 0.2
        if (self.x < 0 - WindowConfig().width*tolerance or
            self.x > WindowConfig().width + WindowConfig().width*tolerance  or
            self.y < 0 - WindowConfig().height*tolerance or
            self.y > WindowConfig().height + WindowConfig().height*tolerance):
            self.queued_for_deletion = True
                    
                    
                    
                    
                    
                    
                    