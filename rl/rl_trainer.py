import pandas as pd
import random
import os
import csv

class RLTrainer:
    """Manages the Q-learning process, including policy updates and learning from rewards."""
    def __init__(self, rl_log_file, performance_log_file, train_mode=False):
        """
        Initializes the trainer.
        Args:
            rl_log_file (str): Path to save/load the Q-table.
            performance_log_file (str): Path to log performance stats (state, action, reward).
            train_mode (bool): If True, forces exploration of untrained actions.
        """
        self.q_table_file = rl_log_file
        self.performance_log_file = performance_log_file
        self.train_mode = train_mode
        self.states = [f"{err}_{stat}" for err in ["deployment_failure", "latency_issue", "anomaly_score", "anomaly_health"] for stat in ["UP", "DOWN"]]
        self.actions = ["retry_deployment", "restore_previous_version", "adjust_thresholds"]
        self.alpha = 0.1
        self.epsilon = 0.1
        self.q_table = self._load_q_table()
        self._initialize_performance_log()
        print("Initialized RL Trainer.")

    def _initialize_performance_log(self):
        """Creates the performance log file with a header if it doesn't exist."""
        os.makedirs(os.path.dirname(self.performance_log_file), exist_ok=True)
        if not os.path.exists(self.performance_log_file):
            with open(self.performance_log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "state", "action", "reward"])

    def _log_performance(self, state, action, reward):
        """Logs a single state, action, and reward tuple to the performance log."""
        timestamp = pd.Timestamp.now().isoformat()
        with open(self.performance_log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, state, action, reward])

    def _load_q_table(self):
        """Loads the Q-table, creating it if it doesn't exist."""
        os.makedirs(os.path.dirname(self.q_table_file), exist_ok=True)
        try:
            qt = pd.read_csv(self.q_table_file, index_col=0)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            qt = pd.DataFrame()
        
        for s in self.states:
            if s not in qt.index: qt.loc[s] = 0.0
        for a in self.actions:
            if a not in qt.columns: qt[a] = 0.0
        
        return qt.loc[self.states, self.actions].fillna(0.0).astype(float)

    def save_q_table(self):
        """Saves the current Q-table to the log file."""
        print(f"\nSaving updated Q-table to {self.q_table_file}")
        self.q_table.to_csv(self.q_table_file)
        print("Save complete.")

    def choose_action(self, state):
        """Chooses an action based on the current policy."""
        if state not in self.q_table.index:
            self.q_table.loc[state] = 0.0
        
        if self.train_mode:
            untrained = self.q_table.loc[state][self.q_table.loc[state] == 0].index.tolist()
            if untrained:
                action = random.choice(untrained)
                print(f"RL Trainer (Training Mode): Forcing untrained action '{action}'")
                return action
        
        if random.uniform(0, 1) < self.epsilon:
            action = random.choice(self.actions)
            print(f"RL Trainer: Exploring -> Randomly chose action '{action}'")
        else:
            action = self.q_table.loc[state].idxmax()
            print(f"RL Trainer: Exploiting -> Chose best action '{action}'")
        return action

    def learn(self, state, action, base_reward, user_feedback=None):
        """
        Updates the Q-table based on the system's result and the user's direct terminal feedback.
        """
        user_reward_bonus = 0
        
        if user_feedback:
            if user_feedback == 'accepted' and base_reward > 0:
                user_reward_bonus = 2
                print(f"User feedback applied: Accepted correct action, applying +2 reward bonus.")
            elif user_feedback == 'rejected':
                base_reward = -1
                print(f"User feedback applied: Rejected action, forcing -1 reward.")

        final_reward = base_reward + user_reward_bonus
        self._log_performance(state, action, final_reward)
        
        old_value = self.q_table.loc[state, action]
        new_value = old_value + self.alpha * (final_reward - old_value)
        self.q_table.loc[state, action] = new_value
        print(f"RL Trainer: Policy updated for state '{state}', action '{action}'. {old_value:.3f} -> {new_value:.3f}")

