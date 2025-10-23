import pandas as pd
import os
import csv
import datetime

class IssueDetector:
    """Reads logs and data to determine the specific type of failure and logs its findings."""
    def __init__(self, log_file, data_file, issue_log_file):
        """
        Initializes the agent with paths to necessary files.
        Args:
            log_file (str): Path to the main deployment log.
            data_file (str): Path to the dataset being monitored.
            issue_log_file (str): Path to log detected issues.
        """
        self.log_file = log_file
        self.data_file = data_file
        self.issue_log_file = issue_log_file

        # Thresholds
        self.latency_threshold_ms = 16000
        self.low_score_threshold = 40
        self.high_hr_threshold = 120
        self.low_o2_threshold = 95

        self._initialize_issue_log()
        print("Initialized Issue Detector Agent.")

    def _initialize_issue_log(self):
        """Creates the issue log file with a header if it doesn't exist."""
        os.makedirs(os.path.dirname(self.issue_log_file), exist_ok=True)
        if not os.path.exists(self.issue_log_file):
            with open(self.issue_log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "failure_state", "reason"])

    def _log_issue(self, state, reason):
        """Logs a detected issue to the issue_log.csv file."""
        timestamp = datetime.datetime.now().isoformat()
        with open(self.issue_log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, state, reason])
        print(f"Issue Detector: Logged issue -> {state}: {reason}")

    def check_data_quality_only(self):
        """
        🔥 NEW METHOD: Checks ONLY for data anomalies (before deployment).
        This ensures anomaly_score and anomaly_health are detected as root causes.
        """
        try:
            if not os.path.exists(self.data_file):
                return "no_failure", "Data file not found."
            
            # Check student scores
            if "student_scores" in self.data_file:
                score_df = pd.read_csv(self.data_file)
                if not score_df.empty and 'score' in score_df.columns:
                    avg_score = score_df['score'].mean()
                    if avg_score < self.low_score_threshold:
                        state, reason = "anomaly_score", f"Low student performance (Avg score={avg_score:.2f})"
                        self._log_issue(state, reason)
                        return state, reason
            
            # Check patient health
            elif "patient_health" in self.data_file:
                health_df = pd.read_csv(self.data_file)
                if not health_df.empty:
                    last_vitals = health_df.iloc[-1]
                    hr = last_vitals.get('heart_rate', 0)
                    o2 = last_vitals.get('oxygen_level', 100)
                    
                    if hr > self.high_hr_threshold:
                        state, reason = "anomaly_health", f"High heart rate detected ({hr})."
                        self._log_issue(state, reason)
                        return state, reason
                    
                    if o2 < self.low_o2_threshold:
                        state, reason = "anomaly_health", f"Low oxygen detected ({o2})."
                        self._log_issue(state, reason)
                        return state, reason

            return "no_failure", "Data quality check passed."

        except (FileNotFoundError, pd.errors.EmptyDataError):
            return "no_failure", "Data file not found or empty."
        except Exception as e:
            return "no_failure", f"Error checking data quality: {e}"

    def check_deployment_issues_only(self):
        """
        🔥 NEW METHOD: Checks ONLY for deployment issues (after deployment).
        This checks deployment failures and latency, not data anomalies.
        """
        try:
            if not os.path.exists(self.log_file):
                return "no_failure", "Deployment log not found."
            
            log_df = pd.read_csv(self.log_file)
            if log_df.empty:
                return "no_failure", "Deployment log is empty."
            
            last_event = log_df.iloc[-1]
            status = str(last_event.get('status', '')).lower().strip()
            rt = pd.to_numeric(last_event.get('response_time_ms'), errors='coerce')

            # Check for deployment failure
            if status == 'failure':
                state, reason = "deployment_failure", "Last deployment attempt failed."
                self._log_issue(state, reason)
                return state, reason
            
            # Check for latency issues
            if pd.notna(rt) and rt > self.latency_threshold_ms:
                state, reason = "latency_issue", f"High latency detected: {rt:.2f} ms."
                self._log_issue(state, reason)
                return state, reason

            return "no_failure", "Deployment successful."

        except (FileNotFoundError, pd.errors.EmptyDataError):
            return "no_failure", "Deployment log not found or empty."
        except Exception as e:
            return "no_failure", f"Error checking deployment: {e}"

    def detect_failure_type(self):
        """
        LEGACY METHOD: Kept for backward compatibility.
        Checks data quality first, then deployment issues.
        """
        # Check data anomalies first
        state, reason = self.check_data_quality_only()
        if state != "no_failure":
            return state, reason
        
        # Then check deployment issues
        return self.check_deployment_issues_only()
    
        # --- NEW: Check for anomaly-based issues ---
        if "anomaly" in self.data_file.lower():
            # You might instead compute mean deviation
            return "anomaly_score", "Detected data anomaly based on statistical deviation."
        
        # If no failure detected
        return "no_failure", "Data quality check passed."
