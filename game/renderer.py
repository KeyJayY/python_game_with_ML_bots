import pygame
from game.simulation import Simulation
from config import (
    PlayerConfig,
    GameConfig,
    Color,
    HealthBarConfig,
    WindowConfig,
    MapConfig,
)
import math


class Renderer:
    def __init__(self, simulation: Simulation):
        pygame.init()

        self.simulation = simulation
        self.screen = pygame.display.set_mode(
            (WindowConfig().width, WindowConfig().height)
        )
        self.clock = pygame.time.Clock()
        self.w_pressed = False
        self.s_pressed = False
        self.a_pressed = False
        self.d_pressed = False
        self.mouse_pressed = False

        self.apply_offsets()

    def draw_player(self):
        self.simulation.player.draw(self.screen, self.offset_x, self.offset_y)

    def draw_bullets(self):
        for bullet in self.simulation.bullets:
            bullet.draw(self.screen, self.offset_x, self.offset_y)

    def draw_map(self):
        for obstacle in self.simulation.map.obstacles:
            pygame.draw.rect(
                self.screen,
                Color().green,
                (
                    obstacle.x - self.offset_x,
                    obstacle.y - self.offset_y,
                    obstacle.width,
                    obstacle.height,
                ),
            )

    def draw_bots(self):
        for bot in self.simulation.bots:
            bot.draw(self.screen, self.offset_x, self.offset_y)
        for bot in self.simulation.player_like_bots:
            bot.draw(self.screen, self.offset_x, self.offset_y)

    def draw_ammo(self):
        font = pygame.font.Font(HealthBarConfig().font, HealthBarConfig.font_size)
        label = f"{self.simulation.player.weapon.magazine} / {self.simulation.player.weapon.magazine_capacity}"
        if self.simulation.player.weapon.realoud_countdown > 0:
            label = (
                f"Reload: {self.simulation.player.weapon.realoud_countdown / 60: .2f}"
            )
        self.screen.blit(
            font.render(label, True, Color().white),
            (WindowConfig().width - 90, 30),
        )

    def draw_healths_bars(self):
        health = self.simulation.player.health
        font = pygame.font.Font(HealthBarConfig().font, HealthBarConfig.font_size)
        label = f"Player: {health} %"
        y = HealthBarConfig().y
        for nr, bot in enumerate(self.simulation.bots):
            self.screen.blit(
                font.render(label, True, Color().white), (HealthBarConfig().x, y - 20)
            )
            pygame.draw.rect(
                self.screen,
                Color().light_blue,
                (HealthBarConfig().x, y, health, HealthBarConfig().height),
            )
            health = bot.health
            y += HealthBarConfig.offset
            label = f"Bot {nr+1}: {health} %"
            # display health for only two bots
            if nr == 2:
                break

    def draw_frame(self):
        self.screen.fill(Color().black)
        self.draw_map()
        self.draw_player()
        self.draw_bullets()
        self.draw_bots()
        self.draw_healths_bars()
        self.draw_ammo()
        pygame.display.flip()

    def handle_mouse_and_keyborad_input(self, event):
        if event.type == pygame.QUIT:
            self.simulation.game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.a_pressed = True
            elif event.key == pygame.K_d:
                self.d_pressed = True
            elif event.key == pygame.K_w:
                self.simulation.player.jump()
            elif event.key == pygame.K_SPACE:
                self.simulation.player.jump()
            elif event.key == pygame.K_ESCAPE:
                self.s_pressed = self.simulation.game_over = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.a_pressed = False
            elif event.key == pygame.K_d:
                self.d_pressed = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.mouse_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.mouse_pressed = False

    def player_move(self):
        if self.a_pressed:
            self.simulation.player.move(False)
        if self.d_pressed:
            self.simulation.player.move(True)

    def player_shoot(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        direction = math.atan2(
            mouse_y
            - (self.simulation.player.y + PlayerConfig().height / 2 - self.offset_y),
            mouse_x
            - (self.simulation.player.x + PlayerConfig().width / 2 - self.offset_x),
        )
        self.simulation.player_shoot(direction)

    def apply_offsets(self):
        self.offset_x = (
            self.simulation.player.x
            + PlayerConfig().width / 2
            - WindowConfig().width / 2
        )
        self.offset_x = max(
            0, min(self.offset_x, MapConfig().width - WindowConfig().width)
        )

        self.offset_y = (
            self.simulation.player.y
            + PlayerConfig().height / 2
            - WindowConfig().height / 2
        )
        self.offset_y = max(
            0, min(self.offset_y, MapConfig().height - WindowConfig().height)
        )

    def run(self):
        while not self.simulation.game_over:
            self.apply_offsets()

            for event in pygame.event.get():
                self.handle_mouse_and_keyborad_input(event)

            self.player_move()

            if self.mouse_pressed:
                self.player_shoot()

            self.draw_frame()
            self.simulation.next_step()
            self.clock.tick(GameConfig().fps)
