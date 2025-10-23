import pandas as pd
import random
import os
import csv
import datetime
from utils import trigger_dashboard_deployment
import shutil

class RLOptimizer:
    """Uses a Q-learning table to choose the best healing strategy and learn from user feedback."""

    def __init__(self, healing_log_file, rl_log_file, feedback_file, train_mode=False):
        """
        Initializes the agent with paths for its logs and Q-table.
        Args:
            healing_log_file (str): Path to log healing attempt outcomes.
            rl_log_file (str): Path to save/load the Q-table CSV.
            feedback_file (str): Path to read user feedback.
            train_mode (bool): If True, forces the agent to try untrained actions.
        """
        self.healing_log_file = healing_log_file
        self.q_table_file = rl_log_file
        self.feedback_file = feedback_file
        self.train_mode = train_mode
        self.states = ["deployment_failure", "latency_issue", "anomaly_score", "anomaly_health"]
        self.actions = ["retry_deployment", "restore_previous_version", "adjust_thresholds"]
        self.alpha = 0.1  # Learning rate
        self.epsilon = 0.1  # Exploration rate
        self._initialize_logs()
        self.q_table = self._load_q_table()
        print("Initialized RL Optimizer Agent.")

    def _initialize_logs(self):
        """Creates log files with headers if they don't exist."""
        for f in [self.healing_log_file, self.feedback_file]:
            os.makedirs(os.path.dirname(f), exist_ok=True)
            if not os.path.exists(f):
                with open(f, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    if "healing" in f:
                        writer.writerow(["timestamp", "strategy", "status", "response_time_ms"])
                    elif "feedback" in f:
                        writer.writerow(["timestamp", "state", "action", "outcome", "feedback"])

    def _log_healing_attempt(self, strategy, status, response_time):
        """Logs the outcome of a single healing attempt."""
        timestamp = datetime.datetime.now().isoformat()
        with open(self.healing_log_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, strategy, status, round(response_time, 2)])

    def _load_q_table(self):
        """Loads the Q-table, creating it if it doesn't exist."""
        os.makedirs(os.path.dirname(self.q_table_file), exist_ok=True)
        try:
            qt = pd.read_csv(self.q_table_file, index_col=0)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            qt = pd.DataFrame()
        
        for a in self.actions:
            if a not in qt.columns: qt[a] = 0.0
        for s in self.states:
            if s not in qt.index: qt.loc[s] = 0.0
        
        return qt.loc[self.states, self.actions].fillna(0.0).astype(float)

    def save_q_table(self):
        """Saves the Q-table to its log file."""
        print(f"\nSaving updated Q-table to {self.q_table_file}")
        self.q_table.to_csv(self.q_table_file)
        print("Save complete.")

    def _apply_user_feedback(self):
        """Checks for and applies user feedback, then clears the feedback file."""
        try:
            if not os.path.exists(self.feedback_file) or os.path.getsize(self.feedback_file) == 0:
                return 

            feedback_df = pd.read_csv(self.feedback_file)
            if feedback_df.empty:
                return
        except pd.errors.EmptyDataError:
            return

        last_feedback = feedback_df.iloc[-1]
        state, action, outcome, feedback = last_feedback['state'], last_feedback['action'], last_feedback['outcome'], last_feedback['feedback']
        
        # User override: if user rejected the fix, the reward is always -1.
        reward = -1 if feedback == 'rejected' else (1 if outcome == 'success' else -1)
        
        print(f"\nApplying user feedback: state='{state}', action='{action}', final_reward={reward}")
        self.update_q_table(state, action, reward)
        
        # Clear the feedback file by re-writing only the header
        with open(self.feedback_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "state", "action", "outcome", "feedback"])
        print("User feedback applied and cleared.")


    def update_q_table(self, state, action, reward):
        """The core Q-learning update rule."""
        if state not in self.q_table.index: self.q_table.loc[state] = 0.0
        old_value = self.q_table.loc[state, action]
        new_value = old_value + self.alpha * (reward - old_value)
        self.q_table.loc[state, action] = new_value
        print(f"RL Optimizer: Q-table updated for state '{state}', action '{action}'. {old_value:.3f} -> {new_value:.3f}")

    def choose_action(self, state):
        """Chooses an action using an epsilon-greedy or training policy."""
        if state not in self.q_table.index: self.q_table.loc[state] = 0.0
        
        if self.train_mode:
            untrained_actions = self.q_table.loc[state][self.q_table.loc[state] == 0].index.tolist()
            if untrained_actions:
                action = random.choice(untrained_actions)
                print(f"RL Optimizer (Training): Forcing untrained action '{action}'")
                return action
        
        if random.uniform(0, 1) < self.epsilon:
            action = random.choice(self.actions)
            print(f"RL Optimizer: Exploring -> Randomly chose action '{action}'")
        else:
            action = self.q_table.loc[state].idxmax()
            print(f"RL Optimizer: Exploiting -> Chose best action '{action}'")
        return action

    def attempt_healing(self, state, dataset_path):
        """Chooses and executes a healing action."""
        self._apply_user_feedback()
        action = self.choose_action(state)
        print(f"\n--- RL Optimizer: Initiating recovery for state '{state}' ---")
        print(f"Chosen Strategy: {action}")
        status, response_time, heal_type = "failure", 0, "unknown_strategy"

        if action == 'retry_deployment':
            status, response_time = trigger_dashboard_deployment(should_fail=False)
            heal_type = "heal_retry"
        elif action == 'restore_previous_version':
            backup_path = f"{dataset_path}.bak"
            if os.path.exists(backup_path):
                shutil.copyfile(backup_path, dataset_path)
                status, response_time = trigger_dashboard_deployment(should_fail=False)
            heal_type = "heal_restore"
        elif action == 'adjust_thresholds':
            status, response_time = "success", 200
            heal_type = "heal_adjust"
        
        self._log_healing_attempt(action, status, response_time)
        return status, response_time, heal_type, action

