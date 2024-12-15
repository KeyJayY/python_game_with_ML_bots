import gym
from gym.spaces import Discrete,Box,Tuple,Dict
import numpy as np
from game.simulation import Simulation
from game.renderer import Renderer

class Environment(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self,render_mode=None):
        self.simulation=Simulation()
        self.renderer = Renderer(self.simulation)

        # Movement actions: none, left, right, jump
        # Shoot actions: vector[dx,dy] in range [-1,1]
        self.action_space=Tuple((Discrete(4),Box(low=-1.0,high=1.0,shape=(2,),dtype=np.float32)))
        
        self.observation_space=Tuple([
            Dict(
                {
                "position": Box(low=-np.inf,high=np.inf,shape=(2,),dtype=np.float32),# (x,y)
                "is_alive": Discrete(2), # 0 or 1
                "health": Box(low=0,high=100,shape=(1,),dtype=np.float32), # health 0-100%
                #TODO: maybe add another observation ?
                }
            )
        ]*2)

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode=render_mode

    def _get_obs(self):
        bots = self.simulation.bots[:2]
        obs=[]
        for bot in bots:
            obs.append(
                {
                    "position": np.array([bot.x,bot.y],dtype=np.float32),
                    "is_alive": 1 if bot.health > 0 else 0,
                    "health": np.array([bot.health],dtype=np.float32),
                }
            )
        return obs
    
    def reset(self,seed=None,options=None):
        super().reset(seed=seed)
        self.simulation.reset()
        observation = self._get_obs()
        return observation, {}
    
    def step(self,action):

        move,shoot=action
        #TODO: implement performing action by agent

        #TODO: next step

        observation=self._get_obs()

        #TODO: implement calculating reward
        reward=self._calculate_reward()

        done=self.simulation.game_over

        return observation, reward, done, {}
    
    def _calculate_reward(self):
        pass

    def render(self):
        if self.render_mode == 'human':
            self.renderer.draw_frame()
        elif self.render_mode == None:
            pass
    
    def close(self):
        self.renderer.close()
