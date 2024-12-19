from gym.envs.registration import register

register(
    id='GameWithMLBots-v0',
    entry_point='environment:Environment'
)
