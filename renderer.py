import pygame
from simulation import Simulation
from bullet import Bullet
import bots
from config import PlayerConfig, GameConfig, Color
import random
from config import PlayerConfig, GameConfig, Color ,HealthBarConfig


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
    
    def draw_healths_bars(self):
        health=self.simulation.player.health
        font =pygame.font.Font(HealthBarConfig().font,HealthBarConfig.font_size)
        label=f"Player: {health} %"
        y=HealthBarConfig().y
        for nr ,bot in enumerate(self.simulation.bots):
            self.screen.blit(
                font.render(
                    label,
                    True,Color().white
                ),
                (
                    HealthBarConfig().x,
                    y-20
                )
            )
            pygame.draw.rect(
                self.screen,
                Color().light_blue,
                (
                    HealthBarConfig().x,
                    y,
                    health,
                    HealthBarConfig().height
                ),
            )
            health=bot.health
            y+=HealthBarConfig.offset
            label=f"Bot {nr+1}: {health} %"
        
    def draw_frame(self):
        self.screen.fill(Color().black)
        for entity in self.simulation.entities:
            entity.draw(self.screen)
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
        dx = 0
        if self.a_pressed:
            dx -= PlayerConfig().speed
        if self.d_pressed:
            dx += PlayerConfig().speed
        self.simulation.player.move(dx, 0)

    def bot_shoot(self):
        mouse_x, mouse_y = self.simulation.player.x, self.simulation.player.y
        if(random.randint(0,4)==1 and  self.simulation.bots):
            self.simulation.entities.append(Bullet(self.simulation.bots[0], mouse_x, mouse_y, "single", "bot1"))

    def run(self):
        while not self.simulation.game_over:
            for event in pygame.event.get():
                self.handle_mouse_and_keyborad_input(event)
            self.player_move()

            for bot in self.simulation.bots:
                bot.move_to_player()

            if self.mouse_pressed:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.simulation.entities.append(
                    Bullet(self.simulation.player, mouse_x, mouse_y, "shotgun")
                )
            self.bot_shoot()
            self.draw_frame()
            self.simulation.next_step()
            self.clock.tick(GameConfig().fps)
