import torch
import torch.nn as nn
import torch.optim as optim
import random
from collections import deque
from config import MLConfig
import numpy as np


class DQN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(DQN, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, output_dim),
        )

    def forward(self, x):
        return self.network(x)


class DQLAgent:
    def __init__(self, ml_config: MLConfig, state_dim: int, action_dim: int):
        self.config = ml_config
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.epsilon = ml_config.epsilon_start
        self.memory = deque(maxlen=ml_config.replay_memory_size)

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.policy_net = DQN(state_dim, action_dim).to(self.device)
        self.target_net = DQN(state_dim, action_dim).to(self.device)

        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=ml_config.lr)
        self.criterion = nn.MSELoss()

        self.timestep = 0

    def select_action(self, state):
        """Select an action based on epsilon-greedy strategy"""
        if random.random() < self.epsilon:
            return random.randint(0, self.action_dim - 1)
        else:
            numeric_state = self._extract_numeric_data(state)
            state_tensor = torch.FloatTensor(numeric_state).unsqueeze(0).to(self.device)
            with torch.no_grad():
                return torch.argmax(self.policy_net(state_tensor)).item()

    def store_experience(self, state, action, reward, next_state, done):
        """Store experience in memory."""
        self.memory.append((state, action, reward, next_state, done))

    def decay_epsilon(self, epsilon_decay, epsilon_min):
        """Decay epsilon for epsilon-greedy strategy."""
        self.epsilon = max(self.epsilon * epsilon_decay, epsilon_min)

    def _extract_numeric_data(self, state):
        if isinstance(state, tuple):
            state = state[0]

        actor = state["actor"]
        actor_position = actor["position"]

        numeric_state = actor_position + [actor["health"], actor["ammo"]]

        numeric_state = np.array(numeric_state)
        if len(numeric_state) < self.state_dim:
            padding = np.zeros(self.state_dim - len(numeric_state))
            numeric_state = np.concatenate((numeric_state, padding))

        return numeric_state

    def train(self, batch_size=64, gamma=0.99, target_update_frequency=10):
        """Train the DQN agent using experience replay."""
        if len(self.memory) < batch_size:
            return

        batch = random.sample(self.memory, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = [self._extract_numeric_data(state) for state in states]
        next_states = [
            self._extract_numeric_data(next_state) for next_state in next_states
        ]

        states = torch.FloatTensor(states).to(self.device)
        actions = torch.LongTensor(actions).unsqueeze(1).to(self.device)
        rewards = torch.FloatTensor(rewards).to(self.device)
        next_states = torch.FloatTensor(next_states).to(self.device)
        dones = torch.FloatTensor(dones).to(self.device)

        current_q = self.policy_net(states).gather(1, actions).squeeze(1)

        next_q = self.target_net(next_states).max(1)[0]

        target_q = rewards + gamma * next_q * (1 - dones)

        loss = self.criterion(current_q, target_q.detach())

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.decay_epsilon(self.config.epsilon_decay, self.config.epsilon_end)

        self.timestep += 1
        if self.timestep % target_update_frequency == 0:
            self.update_target_network()

    def update_target_network(self):
        """Update the target network with the policy network's weights."""
        self.target_net.load_state_dict(self.policy_net.state_dict())

    def get_epsilon(self):
        """Return the current epsilon value."""
        return self.epsilon
