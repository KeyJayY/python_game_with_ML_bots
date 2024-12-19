from config import MapConfig, PlayerConfig, PhysicsConfig
import characters.entity as ent
from characters.bullet import Bullet
from characters.entity import Entity
from characters.weapon import Gun, Shotgun, Auto
from random import randint
from map.obstacle import Obstacle


class Player(ent.Entity):
    def __init__(self):
        super().__init__()
        self.x = randint(0, MapConfig().width - PlayerConfig().width)
        self.y = randint(
            0, MapConfig().height - PlayerConfig().height - Obstacle().height
        )
        self.velocity_y: float = 0
        self.is_falling = False
        self.health = PlayerConfig().health
        self.width = PlayerConfig().width
        self.height = PlayerConfig().height
        self.config = PlayerConfig()
        self.weapons = [
            Auto(self),
            Shotgun(self),
            Gun(self),
        ]
        self.weapon = self.weapons[0]
        self.color = PlayerConfig().color
        self.size = [self.width, self.height]
        self.collision_layer = ent.CollisionLayers.ACTOR
        self.collision_interactions = {
            ent.CollisionLayers.GROUND: ent.CollisionInteractions.STAND,
            ent.CollisionLayers.BULLET: ent.CollisionInteractions.HURT,
        }

    def move(self, right: bool):
        new_x = self.x + PlayerConfig().speed * (1 if right else -1)
        if 0 + self.width / 2 <= new_x <= MapConfig().width - self.width / 2:
            self.x = new_x

    def change_weapon(self, weapon_index: int):
        if self.weapon.reload_countdown > 0:
            self.weapon.reload()
        self.weapon = self.weapons[weapon_index]

    def jump(self):
        if not self.is_falling:
            self.velocity_y = PlayerConfig().initial_jump_velocity
            self.is_falling = True

    def apply_y_movement(self):
        if self.is_falling:
            self.y += self.velocity_y

    def apply_gravity(self):
        if self.is_falling:
            self.velocity_y += PhysicsConfig().gravity

    def shoot(self, direction):
        return self.weapon.shoot(direction)

    def is_reloading(self):
        return 1 if self.weapon.reload_countdown > 0 else 0

    def update(self):
        self.apply_y_movement()
        self.apply_gravity()
        self.is_falling = True

    def reset(self):
        self.x = PlayerConfig().start_x
        self.y = PlayerConfig().start_y
        self.velocity_y: float = 0
        self.is_falling = False
        self.health = PlayerConfig().health
        self.weapon = Shotgun(self)
