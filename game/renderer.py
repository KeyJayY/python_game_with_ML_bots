import pygame
from game.simulation import Simulation
from characters.bullet import Bullet
from config import PlayerConfig, GameConfig, Color, HealthBarConfig
import random
import math


class Renderer:
    def __init__(self, simulation: Simulation):
        pygame.init()

        self.simulation = simulation
        self.screen = pygame.display.set_mode(
            (simulation.map.width, simulation.map.height)
        )
        self.clock = pygame.time.Clock()
        self.w_pressed = False
        self.s_pressed = False
        self.a_pressed = False
        self.d_pressed = False
        self.mouse_pressed = False

    def draw_player(self):
        self.simulation.player.draw(self.screen)

    def draw_bullets(self):
        for bullet in self.simulation.bullets:
            bullet.draw(self.screen)

    def draw_bots_bullets(self):
        for bullet in self.simulation.bots_bullets:
            bullet.draw(self.screen)

    def draw_map(self):
        for obstacle in self.simulation.map.obstacles:
            pygame.draw.rect(
                self.screen,
                Color().green,
                (
                    obstacle.x,
                    obstacle.y,
                    obstacle.width,
                    obstacle.height,
                ),
            )

    def draw_bots(self):
        for bot in self.simulation.bots:
            bot.draw(self.screen)
        for bot in self.simulation.player_like_bots:
            bot.draw(self.screen)

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
        self.draw_bots_bullets()
        self.draw_bots()
        self.draw_healths_bars()
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

    def run(self):
        while not self.simulation.game_over:
            for event in pygame.event.get():
                self.handle_mouse_and_keyborad_input(event)
            self.player_move()

            if self.mouse_pressed:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                direction = math.atan2(
                    mouse_y - (self.simulation.player.y + PlayerConfig().height / 2),
                    mouse_x - (self.simulation.player.x + PlayerConfig().width / 2),
                )
                self.simulation.player_shoot(direction)

            self.draw_frame()
            self.simulation.next_step()
            self.clock.tick(GameConfig().fps)
