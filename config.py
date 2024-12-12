from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class WindowConfig:
    width: int = 1200
    height: int = 700


@dataclass(frozen=True)
class GameConfig:
    fps: int = 60


@dataclass(frozen=True)
class Color:
    black: tuple[int, int, int] = (0, 0, 0)
    red: tuple[int, int, int] = (255, 0, 0)
    green: tuple[int, int, int] = (0, 255, 0)
    blue: tuple[int, int, int] = (0, 0, 255)
    orange: tuple[int, int, int] = (255, 127, 0)
    yellow: tuple[int, int, int] = (255, 255, 0)
    light_blue: tuple[int, int, int] = (30, 144, 255)
    white: tuple[int, int, int] = (255, 255, 255)


@dataclass(frozen=True)
class MapConfig:
    bg_color: tuple[int, int, int] = Color().black
    width = 1600
    height = 900


@dataclass(frozen=True)
class DefaultEntityConfig:
    color: tuple[int, int, int] = (150, 150, 150)
    width: int = 20
    height: int = 20
    start_x: int = 20
    start_y: int = 20
    health: int = 100


@dataclass(frozen=True)
class PlayerConfig:
    color: tuple[int, int, int] = Color().blue
    width: int = 40
    height: int = 40
    speed: int = 5
    initial_jump_velocity: int = -20
    health: int = 100

    @property
    def radius(self) -> float:
        return np.sqrt(self.width**2 + self.height**2) / 2

    @property
    def start_x(self) -> float:
        return (WindowConfig().width - self.width) / 2

    @property
    def start_y(self) -> float:
        return (WindowConfig().height - self.height) / 2


@dataclass(frozen=True)
class BotConfig:
    color: tuple[int, int, int] = Color().red
    width: int = 10
    height: int = 10
    speed: float = PlayerConfig().speed * 0.6
    health: int = 100

    spawn_range: int = 200  # R - r for ring

    @property
    def radius(self) -> float:
        return np.sqrt(self.width**2 + self.height**2) / 2

    @property
    def min_spawn_radius(self) -> float:  # r for ring
        return PlayerConfig().radius + self.radius + self.radius

    @property
    def max_spawn_radius(self) -> float:  # R for ring
        return self.min_spawn_radius + self.spawn_range


@dataclass(frozen=True)
class SprinterBotConfig(BotConfig):
    color: tuple[int, int, int] = Color().orange
    width: int = 5
    height: int = 5
    speed: float = 0.95 * PlayerConfig().speed
    time_to_max_speed: int = 3


@dataclass(frozen=True)
class BulletConfig:
    color: tuple[int, int, int] = Color().yellow
    radius: int = 5
    width: int = 10
    height: int = 10
    speed: int = 15
    damage: int = 10


@dataclass(frozen=True)
class PhysicsConfig:
    gravity: float = 1


@dataclass(frozen=True)
class HealthBarConfig:
    height: int = 10
    width: int = 100
    x: int = 10
    y: int = 20
    offset: int = 40
    font = None
    font_size: int = 20
    
@dataclass(frozen=True)
class ObstacleConfig:
    color: tuple[int, int, int] = Color().green
