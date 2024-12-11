from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class WindowConfig:
    width: int = 1600
    height: int = 900


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
    
@dataclass(frozen=True)
class PlatformConfig:
    color: tuple[int, int, int] = Color().green
    shape : str = "rectangle"

@dataclass(frozen=True)
class PlayerConfig:
    color: tuple[int, int, int] = Color().blue
    size = [40,40]
    shape : str = "rectangle"
    speed: int = 5
    initial_jump_velocity: int = -20
    health: int = 500
    width = 40
    height = 40
    
    

    @property
    def radius(self) -> float:
        return np.sqrt(self.size[0]**2 + self.size[1]**2) / 2

    @property
    def start_x(self) -> float:
        return (WindowConfig().width - self.size[0]) / 2

    @property
    def start_y(self) -> float:
        return (WindowConfig().height - self.size[1]) / 2


@dataclass(frozen=True)
class BulletConfig:
    color: tuple[int, int, int] = Color().yellow
    size = [1,1]
    radius: int = 1
    shape: str = "rectangle"
    speed: int = 10
    damage: int = 10


@dataclass(frozen=True)
class BotConfig:
    color: tuple[int, int, int] = Color().red
    size = [10,10]
    width = 10
    height = 10
    shape: str = "rectangle"
    speed: float = PlayerConfig().speed * 0.6
    health: int = 100

    spawn_range: int = 200  # R - r for ring

    @property
    def radius(self) -> float:
        return np.sqrt(self.size[0]**2 + self.size[1]**2) / 2

    @property
    def min_spawn_radius(self) -> float:  # r for ring
        return PlayerConfig().radius + self.radius + self.radius

    @property
    def max_spawn_radius(self) -> float:  # R for ring
        return self.min_spawn_radius + self.spawn_range


@dataclass(frozen=True)
class SprinterBotConfig(BotConfig):
    color: tuple[int, int, int] = Color().orange
    size = [5,5]
    width = 5
    height = 5
    shape: str = "rectangle"
    speed: float = 0.95 * PlayerConfig().speed
    time_to_max_speed: int = 3


@dataclass(frozen=True)
class PhysicsConfig:
    gravity: float = 1


@dataclass(frozen=True)
class HealthBarConfig:
    height: int = 10
    width: int = 100
    x: int = 10
    y: int = 20
    offset : int = 40
    font = None
    font_size : int = 20
    

