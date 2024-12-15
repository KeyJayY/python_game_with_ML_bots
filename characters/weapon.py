from characters.bullet import Bullet


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
        self.bullets_per_shot = 1
        self.magazine_capacity = 10
        self.magazine = self.magazine_capacity
        self.reload_time = 30
        self.spread_angle = 0
        self.offset = 0
        self.time_between_shots = 20


class Shotgun(Weapon):
    def __init__(self, owner):
        super().__init__(damege=10, owner=owner)
        self.spread_angle = 0.3
        self.offset = 5
        self.bullets_per_shot = 5
        self.magazine_capacity = 10
        self.magazine = self.magazine_capacity
        self.reload_time = 120
        self.time_between_shots = 20


class Auto(Weapon):
    def __init__(self, owner):
        super().__init__(damege=10, owner=owner)
        self.spread_angle = 0.1
        self.offset = 0
        self.bullets_per_shot = 1
        self.magazine_capacity = 30
        self.magazine = self.magazine_capacity
        self.reload_time = 60
        self.time_between_shots = 5
