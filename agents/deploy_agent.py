import os
import csv
import datetime

class DeployAgent:
    """Tracks and logs main deployment events to a CSV file."""
    def __init__(self, log_file):
        self.log_file = log_file
        self._initialize_log_file()
        print("Initialized Deploy Agent.")

    def _initialize_log_file(self):
        """Creates the log file with a header if it doesn't exist."""
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        if not os.path.exists(self.log_file):
            with open(self.log_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["timestamp", "dataset_changed", "status", "response_time_ms", "action_type"])

    def log_deployment(self, dataset, status, response_time, action_type="deploy"):
        """Logs a single event to the deployment log file."""
        timestamp = datetime.datetime.now().isoformat()
        with open(self.log_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, dataset, status, round(response_time, 2), action_type])
        print(f"Logged {action_type} for {os.path.basename(dataset)}: {status} ({round(response_time,2)} ms)")

