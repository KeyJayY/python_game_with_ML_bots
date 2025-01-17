import gym
from gym.spaces import Discrete, Box, Dict
import numpy as np
from game.simulation import Simulation


class Environment(gym.Env):
    metadata = {"render_modes": []}

    def __init__(self, render_mode=None):
        self.simulation = Simulation()
        self.max_obstacles = 20
        self.max_enemies = 10

        # Movement actions
        self.action_space = Dict(
            {
                "move": Discrete(3),  # 0: no move, 1: right, 2: left
                "jump": Discrete(2),  # 0: no jump, 1: jump
                "shoot": Discrete(2),  # 0: no shoot, 1: shoot
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

        assert render_mode is None, "Render mode is not supported."
        self.render_mode = render_mode

    def _get_obs(self):
        obs = {
            "actor": self.simulation.get_actor(),
            "obstacles": self._pad_obstacles(self.simulation.get_obstacles()),
            "enemies": self._pad_enemies(self.simulation.get_enemies()),
        }
        return obs

    def _pad_obstacles(self, obstacles):
        obstacles = np.array(obstacles, dtype=np.float32)
        if len(obstacles) < self.max_obstacles:
            padding = np.zeros(
                (self.max_obstacles - len(obstacles), 4), dtype=np.float32
            )
            obstacles = np.vstack([obstacles, padding])
        return obstacles

    def _pad_enemies(self, enemies):
        enemies = np.array(enemies, dtype=np.float32)
        if len(enemies) < self.max_enemies:
            padding = np.zeros((self.max_enemies - len(enemies), 5), dtype=np.float32)
            enemies = np.vstack([enemies, padding])
        return enemies

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed, options=options)
        self.simulation = Simulation()
        observation = self._get_obs()
        return observation, {}

    def step(self, action):
        move = action["move"]
        jump = action["jump"]
        shoot = action["shoot"]

        if move == 1:
            self.simulation.player.move(True)
        elif move == 2:
            self.simulation.player.move(False)
        if jump == 1:
            self.simulation.player.jump()
        if shoot == 1:
            self.simulation.player.shoot(0)  # Fixed angle shooting

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
        pass

    def close(self):
        pass
