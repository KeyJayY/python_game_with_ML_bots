from machine_learning.dql_agent import DQLAgent
from machine_learning.environment import Environment
from config import MLConfig
import torch
from pathlib import Path

ml_config = MLConfig()
env = Environment()

state_dim = 2 + 1 + 1 + (env.max_obstacles * 4) + (env.max_enemies * 5)
action_dim = 3 * 2 * 2

agent = DQLAgent(ml_config, state_dim, action_dim)

num_episodes = 1000
max_timesteps = 1000

for episode in range(num_episodes):
    state = env.reset()
    total_reward = 0
    done = False

    for t in range(max_timesteps):
        action = agent.select_action(state)

        move = action % 3
        jump = (action // 3) % 2
        shoot = action // 6

        action_dict = {"move": move, "jump": jump, "shoot": shoot}

        next_state, reward, done, _, _ = env.step(action_dict)
        agent.store_experience(state, action, reward, next_state, done)
        agent.train(batch_size=ml_config.batch_size)
        state = next_state
        total_reward += reward

        if done:
            break

    print(f"Episode {episode+1}/{num_episodes}, Total Reward: {total_reward}")

    if (episode + 1) % 100 == 0:
        torch.save(
            agent.policy_net.state_dict(),
            Path("ml_saves") / Path(f"model_episode_{episode+1}.pth"),
        )

agent.epsilon = 0
state = env.reset()
done = False
while not done:
    action = agent.select_action(state)
    move = action % 3
    jump = (action // 3) % 2
    shoot = action // 6
    action_dict = {"move": move, "jump": jump, "shoot": shoot}

    next_state, reward, done, _, _ = env.step(action_dict)
    state = next_state
    env.render()
