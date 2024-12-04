from config_dataclass import PlayerConfig, PhysicsConfig


class Player:
    def __init__(self):
        self.x: int = PlayerConfig().start_x
        self.y: int = PlayerConfig().start_y
        self.velocity_y: int = 0
        self.is_falling = False

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def jump(self):
        if not self.is_falling:
            self.velocity_y = -20
            self.is_falling = True

    def apply_y_movement(self):
        if self.is_falling:
            self.y += self.velocity_y

    def apply_gravity(self):
        if self.is_falling:
            self.velocity_y += PhysicsConfig().gravity
