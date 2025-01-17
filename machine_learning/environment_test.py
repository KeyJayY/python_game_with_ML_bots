from machine_learning.environment import Environment

env = Environment()

obs, info = env.reset()
done = False

while not done:
    action = {
        "move": env.action_space["move"].sample(),
        "jump": env.action_space["jump"].sample(),
        "shoot": env.action_space["shoot"].sample(),
        "shoot_angle": env.action_space["shoot_angle"].sample(),
    }
    obs, reward, done, _, _ = env.step(action)
    print(f"Reward: {reward}, Done: {done}")
    env.render()

env.close()
