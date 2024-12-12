from config import MapConfig, PlayerConfig, PhysicsConfig
import characters.entity as ent
from characters.bullet import Bullet

class Player(ent.Entity):
    def __init__(self):
        super().__init__()
        self.x = PlayerConfig().start_x
        self.y = PlayerConfig().start_y
        self.velocity_y: float = 0
        self.is_falling = False
        self.health = PlayerConfig().health
        self.width = PlayerConfig().width
        self.height = PlayerConfig().height
        self.config = PlayerConfig()
        self.color = PlayerConfig().color
        self.size = [self.width,self.height]
        self.collision_layer = ent.CollisionLayers.PLAYER
        self.collision_interactions = {ent.CollisionLayers.GROUND : ent.CollisionInteractions.STAND,
                                       ent.CollisionLayers.BULLET_BOT : ent.CollisionInteractions.HURT
            }

    def move(self, right: bool):
        new_x = self.x + PlayerConfig().speed * (1 if right else -1)
        if 0 + self.width/2 <= new_x <= MapConfig().width - self.width/2:
            self.x = new_x

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
            
    def shoot(self, direction, mode="single"):
        return Bullet(self,
            direction,
            mode,
            )
    
    def update(self):
        self.apply_y_movement()
        self.apply_gravity()
        self.is_falling = True
