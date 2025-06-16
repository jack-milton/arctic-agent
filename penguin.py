import numpy as np
import random

class Penguin:
    def __init__(self, actions):
        self.state = "idle"
        self.actions = actions
        self.q_table = {}  # {(state): [q_values_for_each_action]}
        self.alpha = 0.1   # learning rate
        self.gamma = 0.9   # discount factor
        self.epsilon = 0.2 # exploration rate

    def get_action(self):
        if self.state not in self.q_table:
            self.q_table[self.state] = [0] * len(self.actions)

        if random.random() < self.epsilon:
            return random.randint(0, len(self.actions) - 1)  # explore
        else:
            return int(np.argmax(self.q_table[self.state]))  # exploit

    def update_q(self, action_index, reward, next_state):
        if next_state not in self.q_table:
            self.q_table[next_state] = [0] * len(self.actions)

        old_value = self.q_table[self.state][action_index]
        next_max = max(self.q_table[next_state])
        new_value = old_value + self.alpha * (reward + self.gamma * next_max - old_value)

        self.q_table[self.state][action_index] = new_value
        self.state = next_state
