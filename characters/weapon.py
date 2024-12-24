from characters.bullet import Bullet
from config import WeaponConfig


class Weapon:
    def __init__(self, damage, owner):
        self.damege = damage
        self.owner = owner
        self.reload_countdown = 0
        self.time_between_shots_countdown = 0
        self.magazine = 0
        self.magazine_capacity = 0
        self.bullets_per_shot = 1
        self.reload_time = 0
        self.spread_angle = 0
        self.offset = 0
        self.time_between_shots = 0

    def shoot(self, direction):
        if self.time_between_shots_countdown <= 0 and self.reload_countdown <= 0:
            if self.magazine >= self.bullets_per_shot:
                self.magazine -= self.bullets_per_shot
            else:
                self.reload()
                return []

            self.time_between_shots_countdown = self.time_between_shots
            return [
                Bullet(self.owner, direction, self.spread_angle, self.offset)
                for _ in range(self.bullets_per_shot)
            ]
        return []

    def reload(self):
        self.magazine = self.magazine_capacity
        self.reload_countdown = self.reload_time

    def update_countdown(self):
        if self.reload_countdown > 0:
            self.reload_countdown -= 1
        if self.time_between_shots_countdown > 0:
            self.time_between_shots_countdown -= 1


class Gun(Weapon):
    def __init__(self, owner):
        super().__init__(damage=10, owner=owner)
        self._load_config(WeaponConfig().Gun())

    def _load_config(self, config: WeaponConfig.Gun):
        self.bullets_per_shot = config.bullets_per_shot
        self.magazine_capacity = config.magazine_capacity
        self.magazine = self.magazine_capacity
        self.offset = config.offset
        self.reload_time = config.reload_time
        self.spread_angle = config.spread_angle
        self.time_between_shots = config.time_between_shots


class Shotgun(Weapon):
    def __init__(self, owner):
        super().__init__(damage=10, owner=owner)
        self._load_config(WeaponConfig().Shotgun())

    def _load_config(self, config: WeaponConfig.Shotgun):
        self.bullets_per_shot = config.bullets_per_shot
        self.magazine_capacity = config.magazine_capacity
        self.magazine = self.magazine_capacity
        self.offset = config.offset
        self.reload_time = config.reload_time
        self.spread_angle = config.spread_angle
        self.time_between_shots = config.time_between_shots


class Auto(Weapon):
    def __init__(self, owner):
        super().__init__(damage=10, owner=owner)
        self._load_config(WeaponConfig().Auto())

    def _load_config(self, config: WeaponConfig.Auto):
        self.bullets_per_shot = config.bullets_per_shot
        self.magazine_capacity = config.magazine_capacity
        self.magazine = self.magazine_capacity
        self.offset = config.offset
        self.reload_time = config.reload_time
        self.spread_angle = config.spread_angle
        self.time_between_shots = config.time_between_shots
