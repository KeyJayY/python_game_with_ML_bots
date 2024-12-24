import gym
from gym.spaces import Discrete, Box, Tuple, Dict
import numpy as np
from game.simulation import Simulation
from game.renderer import Renderer


class Environment(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self, render_mode=None):
        self.simulation = Simulation()
        self.renderer = Renderer(self.simulation)
        self.max_obstacles = 20
        self.max_enemies = 10

        # Movement actions
        self.action_space = Dict(
            {
                "move": Discrete(3),  # 0: no move, 1: right 2: left
                "jump": Discrete(2),  # 0: no jump, 1: jum
                "shoot": Discrete(2),  # 0: no shoot, 1: shoot
                "shoot_angle": Box(
                    low=0, high=2 * np.pi, shape=(), dtype=float
                ),  # shoot angle (0, 2pi)
            }
        )

        self.observation_space = Dict(
            {
                "actor": Dict(
                    {
                        "position": Box(
                            low=-np.inf, high=np.inf, shape=(2,), dtype=np.float32
                        ),  # (x, y)
                        "health": Box(low=0, high=100, shape=(), dtype=np.float32),
                        "ammo": Box(low=0, high=100, shape=(), dtype=np.float32),
                        "isReloading": Discrete(2),  #  0 or 1
                    }
                ),
                "obstacles": Box(
                    low=-np.inf,
                    high=np.inf,
                    shape=(self.max_obstacles, 4),
                    dtype=np.float32,
                ),  # (x, y, height, width)
                "enemies": Box(
                    low=-np.inf,
                    high=np.inf,
                    shape=(self.max_enemies, 5),
                    dtype=np.float32,
                ),  # (x, y, height, width, health)
            }
        )

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

    def _get_obs(self):
        obs = {
            "actor": self.simulation.get_actor(),
            "obstacles": self.simulation.get_obstacles(),
            "enemies": self.simulation.get_enemies(),
        }
        return obs

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed, options=options)
        self.simulation = Simulation()
        observation = self._get_obs()
        return observation, {}

    def step(self, action):
        move = action["move"]
        jump = action["jump"]
        shoot = action["shoot"]
        shoot_angle = action["shoot_angle"]

        if move == 1:
            self.simulation.player.move(True)
        elif move == 2:
            self.simulation.player.move(False)
        if jump == 1:
            self.simulation.player.jump()
        if shoot == 1:
            self.simulation.player.shoot(shoot_angle)
        self.simulation.next_step()
        observation = self._get_obs()
        reward = self._calculate_reward()
        done = self.simulation.game_over
        return observation, reward, done, False, {}

    def _calculate_reward(self):
        reward = 0
        if self.simulation.player.last_frame_bullet_hit:
            reward += 1
        if self.simulation.player.get_hit_last_frame:
            reward -= 2
        if self.simulation.player.last_frame_bullet_kill:
            reward += 10
        if self.simulation.game_over and self.simulation.player.health > 0:
            reward += 100
        if self.simulation.game_over and self.simulation.player.health <= 0:
            reward -= 100

        self.simulation.player.last_frame_bullet_hit = False
        self.simulation.player.get_hit_last_frame = False
        self.simulation.player.last_frame_bullet_kill = False

        return reward

    def render(self):
        if self.render_mode == "human":
            self.renderer.draw_frame()
        elif self.render_mode == None:
            pass

    def close(self):
        self.renderer.close()


env = Environment()
print(env._get_obs())
