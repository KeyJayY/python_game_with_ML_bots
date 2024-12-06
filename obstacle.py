from dataclasses import dataclass
import numpy as np
from config import MapConfig, PlayerConfig


@dataclass
class Obstacle:
    x: int = 0
    y: int = 0
    width: int = 20
    height: int = 20
    floor: int = 0
    

    def __post_init__(self):
        self.y = (
            MapConfig().height
            - self.height
            - self.floor * (3 * PlayerConfig().height + self.height)
        )


@dataclass
class ObstaclePlatformShort(Obstacle):
    def __post_init__(self):
        super().__post_init__()
        self.width: int = 100


@dataclass
class ObstaclePlatformLong(Obstacle):
    def __post_init__(self):
        super().__post_init__()
        self.width: int = 300


@dataclass
class ObstacleFloor(Obstacle):
    def __post_init__(self):
        super().__post_init__()
        self.width = MapConfig().width
        self.y = MapConfig().height - self.height


def main() -> None:
    print(ObstacleFloor())


if __name__ == "__main__":
    main()
