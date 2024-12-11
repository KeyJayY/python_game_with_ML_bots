from config import PlayerConfig, PhysicsConfig
import entity as ent


class Player(ent.Entity):
    def __init__(self):
        super().__init__()
        self.x = PlayerConfig().start_x
        self.y = PlayerConfig().start_y
        self.is_falling = False
        self.velocity_y: float = 0
        self.health = PlayerConfig().health
        self.shape = PlayerConfig().shape
        self.size = PlayerConfig().size
        self.collision_layer = ent.Collision_layers.PLAYER
        self.collision_interactions = {
            ent.Collision_layers.GROUND : ent.Collision_interactions.STAND,
            ent.Collision_layers.BULLET_BOT : ent.Collision_interactions.HURT,
            ent.Collision_layers.WALL : ent.Collision_interactions.BLOCK
            }
        self.color = PlayerConfig().color
        
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
        else:
            self.velocity_y = 0

    def apply_gravity(self):
        if self.is_falling:
            self.velocity_y += PhysicsConfig().gravity
    
    def rect(self):
        return[{
            "x" : self.x,
            "y" : self.y,
            "width" : PlayerConfig().width,
            "height" : PlayerConfig().height
        }]

    def reduce_health(self,damage):
        if(self.health - damage < 0):
            self.health = 0
        else:
            self.health -= damage

    def update(self):
        self.apply_y_movement()
        self.apply_gravity()
        self.is_falling = True
