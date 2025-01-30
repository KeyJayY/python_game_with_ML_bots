import re
from game.simulation import Simulation
from machine_learning.dql_agent import DQLAgent
from machine_learning.environment import Environment
from config import MLConfig
import torch
from pathlib import Path


def load_checkpoint(agent, filepath):
    checkpoint = torch.load(filepath, map_location=agent.device, weights_only=True)
    agent.policy_net.load_state_dict(checkpoint["policy_net_state_dict"])
    agent.target_net.load_state_dict(checkpoint["target_net_state_dict"])
    agent.optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
    agent.epsilon = checkpoint["epsilon"]
    agent.timestep = checkpoint["timestep"]

def load_dqn_model(env: Environment):
    ml_config = MLConfig()
    state_dim = 2 + 1 + 1 + (env.max_obstacles * 4) + (env.max_enemies * 5)
    action_dim = 3 * 2 * 2

    agent = DQLAgent(ml_config, state_dim, action_dim)

    checkpoint_dir = Path("ml_saves")
    checkpoint_path, _ = find_latest_checkpoint(checkpoint_dir)
    if checkpoint_path.exists():
        load_checkpoint(agent, checkpoint_path)

    return agent


def find_latest_checkpoint(directory: Path) -> tuple[Path, int]:
    pattern = re.compile(r"model_episode_(\d+)\.pth")
    max_episode = -1
    latest_checkpoint = Path()

    for file in directory.glob("*.pth"):
        match = pattern.search(file.name)
        if match:
            episode = int(match.group(1))
            if episode > max_episode:
                max_episode = episode
                latest_checkpoint = file

    return latest_checkpoint, max_episode


checkpoint_dir = Path("ml_saves")
checkpoint_path, start_episode = find_latest_checkpoint(checkpoint_dir)
ml_config = MLConfig()
env = Environment(Simulation())

state_dim = 2 + 1 + 1 + (env.max_obstacles * 4) + (env.max_enemies * 5)
action_dim = 3 * 2 * 2

agent = DQLAgent(ml_config, state_dim, action_dim)
# Loaded checkpoint: episode: 100, timestep=93_829
# Loaded checkpoint: episode: 200, timestep=186_402
# Loaded checkpoint: episode: 300, timestep=280_572
# Loaded checkpoint: episode: 400, timestep=373_986
# Loaded checkpoint: episode: 500, timestep=465_398
# Loaded checkpoint: episode: 600, timestep=556_939
# Loaded checkpoint: episode: 700, timestep=647_623
num_episodes = 1000
max_timesteps = 1000

if checkpoint_path.exists():
    load_checkpoint(agent, checkpoint_path)
    print(f"Loaded checkpoint: episode: {start_episode:_}, timestep={agent.timestep:_}")
else:
    print("No saved model. Starting training from scratch.")
    start_episode = 0
    
for episode in range(start_episode, num_episodes + 1):

    state = env.reset()
    total_reward = 0
    done = False
    agent.epsilon = agent.config.epsilon_start

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
        agent.save_checkpoint(Path(f"ml_saves/model_episode_{episode+1}.pth"))
        print(f"Saved checkpoint to ml_saves/model_episode_{episode+1}.pth")
        break

agent.epsilon = 0
state = env.reset()
done = False
time = 0
while not done:
    time += 1
    print(f"time: {time}")
    action = agent.select_action(state)
    move = action % 3
    jump = (action // 3) % 2
    shoot = action // 6
    action_dict = {"move": move, "jump": jump, "shoot": shoot}

    next_state, reward, done, _, _ = env.step(action_dict)
    state = next_state
    env.render()
