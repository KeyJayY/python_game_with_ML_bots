from config import MapConfig, PlayerConfig, PhysicsConfig
from characters.entity import Entity


class Player(Entity):
    def __init__(self):
        self.x = PlayerConfig().start_x
        self.y = PlayerConfig().start_y
        self.velocity_y: float = 0
        self.is_falling = False
        self.health = PlayerConfig().health
        self.width = PlayerConfig().width
        self.height = PlayerConfig().height
        self.config = PlayerConfig()

    def move(self, right: bool):
        new_x = self.x + PlayerConfig().speed * (1 if right else -1)
        if 0 <= new_x <= MapConfig().width - self.width:
            self.x = new_x

    def jump(self):
        if not self.is_falling:
            self.velocity_y = PlayerConfig().initial_jump_velocity
            self.is_falling = True

    def rect(self):
        return [
            self,
        ]

    def apply_y_movement(self):
        if self.is_falling:
            self.y += self.velocity_y

    def apply_gravity(self):
        if self.is_falling:
            self.velocity_y += PhysicsConfig().gravity

    def reduce_health(self, damage: float):
        if self.health - damage < 0:
            self.health = 0
        else:
            self.health -= damage
