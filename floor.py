import entity as ent
from config import PlatformConfig


class Platform(ent.Entity):
    def __init__(self,obstacle):
        super().__init__()
        self.collision_layer = ent.Collision_layers.GROUND
        self.color = PlatformConfig().color
        self.shape = PlatformConfig().shape
        self.size = [obstacle["width"],obstacle["height"]]
        self.x = obstacle["width"]/2 + obstacle["x"]
        self.y = obstacle["height"]/2 + obstacle["y"]

class Wall(ent.Entity):
    def __init__(self,obstacle):
        super().__init__()
        self.collision_layer = ent.Collision_layers.WALL | ent.Collision_layers.GROUND
        self.shape = PlatformConfig().shape
        self.color = PlatformConfig().color
        self.size = [obstacle["width"],obstacle["height"]]
        self.x = obstacle["width"]/2 + obstacle["x"]
        self.y = obstacle["height"]/2 + obstacle["y"]