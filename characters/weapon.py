from characters.bullet import Bullet
from config import WeaponConfig


class Weapon:
    def __init__(self, damege, owner):
        self.damege = damege
        self.owner = owner
        self.reload_countdown = 0
        self.time_between_shots_countdown = 0

    def shoot(self, direction):
        if self.time_between_shots_countdown <= 0 and self.reload_countdown <= 0:
            self.magazine -= self.bullets_per_shot
            if self.magazine <= 0:
                self.reload()
            self.time_between_shots_countdown = self.time_between_shots
            return [
                Bullet(self.owner, direction, self.spread_angle, self.offset)
                for _ in range(self.bullets_per_shot)
            ]
        else:
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
        super().__init__(damege=10, owner=owner)
        self.bullets_per_shot = WeaponConfig().Gun().bullets_per_shot
        self.magazine_capacity = WeaponConfig().Gun().magazine_capacity
        self.magazine = self.magazine_capacity
        self.offset = WeaponConfig().Gun().offset
        self.reload_time = WeaponConfig().Gun().reload_time
        self.spread_angle = WeaponConfig().Gun().spread_angle
        self.time_between_shots = WeaponConfig().Gun().time_between_shots


class Shotgun(Weapon):
    def __init__(self, owner):
        super().__init__(damege=10, owner=owner)
        self.bullets_per_shot = WeaponConfig().Shotgun().bullets_per_shot
        self.magazine_capacity = WeaponConfig().Shotgun().magazine_capacity
        self.magazine = self.magazine_capacity
        self.offset = WeaponConfig().Shotgun().offset
        self.reload_time = WeaponConfig().Shotgun().reload_time
        self.spread_angle = WeaponConfig().Shotgun().spread_angle
        self.time_between_shots = WeaponConfig().Shotgun().time_between_shots


class Auto(Weapon):
    def __init__(self, owner):
        super().__init__(damege=10, owner=owner)
        self.bullets_per_shot = WeaponConfig().Auto().bullets_per_shot
        self.magazine_capacity = WeaponConfig().Auto().magazine_capacity
        self.magazine = self.magazine_capacity
        self.offset = WeaponConfig().Auto().offset
        self.reload_time = WeaponConfig().Auto().reload_time
        self.spread_angle = WeaponConfig().Auto().spread_angle
        self.time_between_shots = WeaponConfig().Auto().time_between_shots
