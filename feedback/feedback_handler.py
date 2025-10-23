# rl/feedback_handler.py

import csv
import os
from datetime import datetime

class FeedbackHandler:
    def __init__(self, feedback_file):
        self.feedback_file = feedback_file
        if not os.path.exists(feedback_file):
            with open(feedback_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "state", "action", "outcome", "feedback_source", "feedback_value", "reward"])

    def log_feedback(self, state, action, outcome, feedback_source, feedback_value):
        """Logs both user and simulated feedback with appropriate reward weighting."""
        reward = self.calculate_reward(outcome, feedback_value)
        with open(self.feedback_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(),
                state,
                action,
                outcome,
                feedback_source,
                feedback_value,
                reward
            ])
        return reward

    def calculate_reward(self, outcome, feedback_value):
        """Dynamically adjusts reward."""
        # base reward from outcome
        base = 1 if outcome == 'success' else -1
        if feedback_value == "positive":
            base += 2
        elif feedback_value == "neutral":
            base += 0
        elif feedback_value == "negative":
            base -= 1
        return base

    def get_latest_feedback(self):
        """Optional: read most recent feedback entry."""
        try:
            with open(self.feedback_file, "r") as f:
                lines = f.readlines()
            return lines[-1].strip().split(",") if len(lines) > 1 else None
        except Exception:
            return None
