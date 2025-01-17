from machine_learning.environment import Environment
import numpy as np


def test_environment():
    env = Environment()

    print("=== Testing Environment Reset ===")
    observation, _ = env.reset()
    print("Initial Observation:", observation)

    print("\n=== Testing Step Function ===")
    test_action = {"move": 1, "jump": 0, "shoot": 1}  # Example action
    next_obs, reward, done, _, _ = env.step(test_action)
    print("Next Observation:", next_obs)
    print("Reward:", reward)
    print("Done:", done)

    print("\n=== Testing Full Episode ===")
    total_reward = 0
    observation, _ = env.reset()
    for _ in range(100):  # Run for 100 steps
        action = {
            "move": np.random.randint(0, 3),
            "jump": np.random.randint(0, 2),
            "shoot": np.random.randint(0, 2),
        }
        observation, reward, done, _, _ = env.step(action)
        total_reward += reward
        if done:
            break
    print("Total Reward for Episode:", total_reward)


if __name__ == "__main__":
    test_environment()
