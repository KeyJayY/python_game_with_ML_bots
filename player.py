from config import PlayerConfig, PhysicsConfig


class Player:
    def __init__(self):
        self.x = PlayerConfig().start_x
        self.y = PlayerConfig().start_y
        self.velocity_y: float = 0
        self.is_falling = False

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

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
