import pygame
import math
import random

from config import PlayerConfig, BulletConfig,BotConfig


class Bullet:
    def __init__(self, player, mouse_x, mouse_y, mode="single", type="player"):
        self.player_width=PlayerConfig().width
        self.player_height=PlayerConfig().height
        self.bot_width=BotConfig().width
        self.bot_height=BotConfig().height
        if(type=="player"):
            self.x = player.x + self.player_width/2
            self.y = player.y + self.player_width/2
        elif (type=="bot1"):
            self.x = player.x + self.bot_width/2
            self.y = player.y + self.bot_width/2
        self.x_direction = mouse_x - self.x
        self.y_direction = mouse_y - self.y
        self.mode=mode
        self.damage=BulletConfig().damage
        

        direction_lenght = math.sqrt(self.x_direction**2 + self.y_direction**2)
        if direction_lenght != 0:
            self.x_direction /= direction_lenght
            self.y_direction /= direction_lenght

        if mode=="shotgun":
            spread_angle=10
            angle = math.atan2(self.y_direction, self.x_direction)
            spread = math.radians(random.uniform(-spread_angle, spread_angle))  
            angle += spread
            self.x_shotgun_direction = math.cos(angle)
            self.y_shotgun_direction = math.sin(angle)

    def update(self):
        if self.mode=="single":
            self.x += self.x_direction * BulletConfig().speed
            self.y += self.y_direction * BulletConfig().speed
        elif self.mode=="shotgun":
            self.x += self.x_shotgun_direction * (BulletConfig().speed-4)
            self.y += self.y_shotgun_direction * (BulletConfig().speed-4)


    def draw(self, screen):
        pygame.draw.circle(
            screen,
            BulletConfig().color,
            (int(self.x), int(self.y)),
            BulletConfig().radius,
        )
    def check_bullet_collision_with_obstacles(self, obstacles):
        bullet_left = self.x - BulletConfig.radius
        bullet_right = self.x + BulletConfig.radius
        bullet_top = self.y - BulletConfig.radius
        bullet_bottom = self.y + BulletConfig.radius

        for obstacle in obstacles:
            obstacle_left = obstacle["x"]
            obstacle_right = obstacle["x"] + obstacle["width"]
            obstacle_top = obstacle["y"]
            obstacle_bottom = obstacle["y"] + obstacle["height"]
            if not (bullet_right <= obstacle_left or  
                    bullet_left >= obstacle_right or  
                    bullet_bottom <= obstacle_top or  
                    bullet_top >= obstacle_bottom):   
                return True
              
        return False
    

