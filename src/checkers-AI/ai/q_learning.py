import random
from collections import deque
import numpy as np
from ai.model import build_q_network
import os
from game.board import *

class QLearningAgent:
    """
    Q-Learning agent with vectorized experience replay and fixed-size buffer.
    Trains once per episode to reduce overhead and uses batch updates.
    """
    def __init__(self,
                 state_shape,
                 action_size,
                 gamma=0.95,
                 epsilon=1.0,
                 epsilon_min=0.01,
                 epsilon_decay=0.995,
                 memory_size=20000,
                 batch_size=64):
        print("[DEBUG] Initializing QLearningAgent...")
        self.state_shape = state_shape
        self.action_size = action_size
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.batch_size = batch_size

        self.memory = deque(maxlen=memory_size)
        print("[DEBUG] Building Q-network...")
        self.model = build_q_network(self.state_shape, self.action_size)

        self.total_rewards = []
        self.loss_history = []
        self.epsilon_history = [self.epsilon]
        self.episode_count = 0
        print("[DEBUG] Agent initialized successfully.")

    def act(self, state):
        if np.random.rand() < self.epsilon:
            action = random.randrange(self.action_size)
            print(f"[DEBUG] Random action chosen: {action}")
            return action
        q_values = self.model.predict(state[np.newaxis, ...], verbose=0)[0]
        action = int(np.argmax(q_values))
        print(f"[DEBUG] Greedy action chosen: {action}")
        return action

    def remember(self, state, action, reward, next_state, done):
        print(f"[DEBUG] Remembering experience. Done: {done}")
        self.memory.append((state, action, reward, next_state, done))

    def replay(self):
        if len(self.memory) < self.batch_size:
            print(f"[DEBUG] Not enough memory to replay. Memory size: {len(self.memory)}")
            return

        print("[DEBUG] Starting replay training...")
        batch = random.sample(self.memory, self.batch_size)
        states = np.array([b[0] for b in batch])
        actions = np.array([b[1] for b in batch])
        rewards = np.array([b[2] for b in batch])
        next_states = np.array([b[3] for b in batch])
        dones = np.array([b[4] for b in batch])

        q_current = self.model.predict(states, verbose=0)
        q_next = self.model.predict(next_states, verbose=0)

        q_target = q_current.copy()
        for i in range(self.batch_size):
            if dones[i]:
                q_target[i, actions[i]] = rewards[i]
            else:
                q_target[i, actions[i]] = rewards[i] + self.gamma * np.max(q_next[i])

        history = self.model.fit(states, q_target, verbose=0)
        loss = history.history['loss'][0]
        self.loss_history.append(loss)
        print(f"[DEBUG] Training loss: {loss}")

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
            self.epsilon_history.append(self.epsilon)
            print(f"[DEBUG] Epsilon decayed to: {self.epsilon}")

    def train_episode(self, env):
        print("[DEBUG] Starting training episode...")
        state = env.reset()
        total_reward = 0
        done = False
        step_count = 0
        max_steps = 500  

        while not done:
            if step_count >= max_steps:
                print(f"[DEBUG] Max steps ({max_steps}) reached, ending episode early.")
                break

            action = self.act(state)
            next_state, reward, done, _ = env.step(action)
            print(f"[DEBUG] Step {step_count} | Action: {action}, Reward: {reward}, Done: {done}")
            self.remember(state, action, reward, next_state, done)
            total_reward += reward
            state = next_state
            step_count += 1

        self.replay()

        self.total_rewards.append(total_reward)
        self.episode_count += 1
        print(f"[DEBUG] Episode {self.episode_count} completed. Reward: {total_reward:.2f}, Loss: {self.loss_history[-1]:.4f}, Epsilon: {self.epsilon:.3f}")
        return total_reward


    def train(self, env, num_episodes=200):
        print(f"[DEBUG] Training started for {num_episodes} episodes...")
        for ep in range(num_episodes):
            print(f"[DEBUG] === Episode {ep+1} ===")
            self.train_episode(env)

    def plot_training(self):
        try:
            import matplotlib.pyplot as plt
            plt.figure(figsize=(12,4))

            plt.subplot(1,3,1)
            plt.plot(self.total_rewards)
            plt.title('Total Rewards')
            plt.xlabel('Episode')
            plt.ylabel('Reward')

            plt.subplot(1,3,2)
            plt.plot(self.loss_history)
            plt.title('Loss History')
            plt.xlabel('Training Step')
            plt.ylabel('Loss')

            plt.subplot(1,3,3)
            plt.plot(self.epsilon_history)
            plt.title('Epsilon Decay')
            plt.xlabel('Training Step')
            plt.ylabel('Epsilon')

            plt.tight_layout()
            plt.show()
        except ImportError:
            print("Matplotlib is required for plotting. Install with 'pip install matplotlib'.")

    def save(self, path):
        """Save model weights and training metadata."""
        # ensure the filename ends with .weights.h5
        if not path.endswith(".weights.h5"):
            base, _ = os.path.splitext(path)
            path = base + ".weights.h5"

        self.model.save_weights(path)
        print(f"Model saved to {path}. Episodes: {self.episode_count}, "
              f"Memory size: {len(self.memory)}, Final epsilon: {self.epsilon:.3f}")

    def load(self, path):
        self.model.load_weights(path)
        print(f"[DEBUG] Loaded model weights from {path}.")

    def get_move(self, board):
        
        from utils.helpers import state_to_input
        state = state_to_input(board.board)
        act = self.act(state)
        n = ROWS * COLS
        start_flat, end_flat = divmod(act, n)
        sr, sc = divmod(start_flat, COLS)
        er, ec = divmod(end_flat, COLS)
        return (sr, sc, er, ec)