import json
from config import MapConfig
from map.obstacle import (
    Obstacle,
    ObstacleFloor,
    ObstaclePlatformLong,
    ObstaclePlatformShort,
)


class Map:
    def __init__(self):
        self.width = MapConfig().width
        self.height = MapConfig().height

        self.obstacles: list[Obstacle] = []

        self.obstacles.append(ObstacleFloor())
        self.obstacles.append(ObstaclePlatformShort(x=50, floor=1))
        self.obstacles.append(ObstaclePlatformLong(x=300, floor=1))
        self.obstacles.append(ObstaclePlatformShort(x=900, floor=1))
        self.obstacles.append(ObstaclePlatformLong(x=1300, floor=1))

        self.obstacles.append(ObstaclePlatformLong(x=0, floor=2))
        self.obstacles.append(ObstaclePlatformLong(x=500, floor=2))
        self.obstacles.append(ObstaclePlatformLong(x=1000, floor=2))
        self.obstacles.append(ObstaclePlatformLong(x=1500, floor=2))

        self.obstacles.append(ObstaclePlatformShort(x=100, floor=3))
        self.obstacles.append(ObstaclePlatformLong(x=300, floor=3))
        self.obstacles.append(ObstaclePlatformShort(x=700, floor=3))
        self.obstacles.append(ObstaclePlatformShort(x=900, floor=3))
        self.obstacles.append(ObstaclePlatformLong(x=1200, floor=3))
