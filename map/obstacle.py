from dataclasses import dataclass
from config import MapConfig, PlayerConfig, ObstacleConfig
import characters.entity as ent
import pygame


class Obstacle(ent.Entity):
    def __init__(self, x=0, floor=0):
        super().__init__()
        self.x = x + self.width / 2
        self.floor = floor
        self.config = ObstacleConfig()
        self.size = [self.width, self.height]
        self.y = (
            MapConfig().height
            - self.height / 2 * 3
            - self.floor * (3 * PlayerConfig().height + self.height)
        )
        self.collision_layer = ent.CollisionLayers.GROUND

    def draw(self, screen, offset_x=0, offset_y=0):
        pygame.draw.rect(
            screen,
            self.config.color,
            (
                self.x - self.size[0] / 2 - offset_x,
                self.y - self.size[1] / 2 - offset_y,
                self.size[0],
                self.size[1],
            ),
        )


class ObstaclePlatformShort(Obstacle):
    def __init__(self, x=0, floor=0):
        super().__init__(x, floor)
        self.width: int = 100
        self.size = [self.width, self.height]
        self.x = x + self.width / 2


class ObstaclePlatformLong(Obstacle):
    def __init__(self, x=0, floor=0):
        super().__init__(x, floor)
        self.width: int = 300
        self.size = [self.width, self.height]
        self.x = x + self.width / 2


class ObstacleFloor(Obstacle):
    def __init__(self, x=0, floor=0):
        super().__init__(x, floor)
        self.width = MapConfig().width
        self.y = MapConfig().height - self.height / 2
        self.size = [self.width, self.height]
        self.x = x + self.width / 2


def main() -> None:
    print(ObstacleFloor())


if __name__ == "__main__":
    main()
