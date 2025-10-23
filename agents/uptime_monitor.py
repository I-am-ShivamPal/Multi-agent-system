import os
import csv
import datetime

class UptimeMonitor:
    """Maintains a synthetic uptime/downtime timeline."""
    def __init__(self, timeline_file):
        """
        Initializes the agent with the full path to the uptime timeline file.
        Args:
            timeline_file (str): The path to the uptime log file (e.g., 'logs/uptime_log.csv').
        """
        self.timeline_file = timeline_file
        self.last_status = self._get_initial_status()
        if self.last_status is None:
            print(f"Initialized uptime timeline: {self.timeline_file}")
            self.update_status("UP", "Initial status check")
        print("Initialized Uptime Monitor Agent.")

    def _get_initial_status(self):
        """Reads the last known status from the timeline file."""
        # Ensure the directory for the log file exists.
        os.makedirs(os.path.dirname(self.timeline_file), exist_ok=True)

        if not os.path.exists(self.timeline_file):
            with open(self.timeline_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'status', 'event'])
            return None
        else:
            try:
                with open(self.timeline_file, 'r', newline='') as f:
                    # Read all rows and get the last one's status
                    rows = list(csv.reader(f))
                    # Handle empty file or header-only file
                    if len(rows) > 1:
                        return rows[-1][1]
                    else:
                        return None
            except (IOError, IndexError):
                return None

    def update_status(self, new_status, event_description):
        """Logs a status change to the timeline if the status is different."""
        if new_status != self.last_status:
            timestamp = datetime.datetime.now().isoformat()
            with open(self.timeline_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, new_status, event_description])
            print(f"Uptime Monitor: Service status changed to {new_status}. Reason: {event_description}")
            self.last_status = new_status
        else:
            print(f"Uptime Monitor: Service status remains {self.last_status}.")

