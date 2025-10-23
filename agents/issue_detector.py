import pandas as pd
import os
import csv
import datetime

class IssueDetector:
    """Detects failures based on configurable thresholds from config.py."""

    def __init__(self, log_file, data_file, issue_log_file, config):
        """
        Initializes with config thresholds (not hardcoded).
        Args:
            log_file (str): Path to deployment log.
            data_file (str): Path to dataset being monitored.
            issue_log_file (str): Path to log detected issues.
            config (dict): Config dictionary containing thresholds.
        """
        self.log_file = log_file
        self.data_file = data_file
        self.issue_log_file = issue_log_file

        # ✅ Load thresholds dynamically
        self.latency_threshold_ms = config.get("latency_ms", 24000)
        self.low_score_threshold = config.get("low_score_avg", 40)
        self.high_hr_threshold = config.get("high_heart_rate", 120)
        self.low_o2_threshold = config.get("low_oxygen_level", 95)

        # Warn for missing keys
        for key in ["latency_ms", "low_score_avg", "high_heart_rate", "low_oxygen_level"]:
            if key not in config:
                print(f"⚠️ Warning: '{key}' not found in config. Using default value.")

        self._initialize_issue_log()
        print("✅ Initialized Issue Detector Agent (Configurable).")

    def _initialize_issue_log(self):
        """Create issue log file if missing."""
        os.makedirs(os.path.dirname(self.issue_log_file), exist_ok=True)
        if not os.path.exists(self.issue_log_file):
            with open(self.issue_log_file, "w", newline="") as f:
                csv.writer(f).writerow(["timestamp", "failure_state", "reason"])

    def _log_issue(self, state, reason):
        """Append detected issue."""
        with open(self.issue_log_file, "a", newline="") as f:
            csv.writer(f).writerow([datetime.datetime.now().isoformat(), state, reason])
        print(f"Issue Detector: Logged issue -> {state}: {reason}")

    def detect_failure_type(self):
        """Check data anomalies first, then deployment issues."""
        try:
            # === 1️⃣ Data-based anomaly detection ===
            if os.path.exists(self.data_file):
                if "student_scores" in self.data_file:
                    df = pd.read_csv(self.data_file)
                    if not df.empty and "score" in df.columns:
                        avg_score = df["score"].mean()
                        if avg_score < self.low_score_threshold:
                            state, reason = "anomaly_score", f"Low student performance (avg={avg_score:.2f})"
                            self._log_issue(state, reason)
                            return state, reason

                elif "patient_health" in self.data_file:
                    df = pd.read_csv(self.data_file)
                    if not df.empty:
                        hr = df.iloc[-1].get("heart_rate", 0)
                        o2 = df.iloc[-1].get("oxygen_level", 100)
                        if hr > self.high_hr_threshold:
                            state, reason = "anomaly_health", f"High heart rate detected ({hr})."
                            self._log_issue(state, reason)
                            return state, reason
                        if o2 < self.low_o2_threshold:
                            state, reason = "anomaly_health", f"Low oxygen detected ({o2})."
                            self._log_issue(state, reason)
                            return state, reason

            # === 2️⃣ Deployment-based issue detection ===
            if os.path.exists(self.log_file):
                df = pd.read_csv(self.log_file)
                if not df.empty:
                    last = df.iloc[-1]
                    status = str(last.get("status", "")).lower().strip()
                    rt = pd.to_numeric(last.get("response_time_ms"), errors="coerce")
                    if status == "failure":
                        state, reason = "deployment_failure", "Last deployment attempt failed."
                        self._log_issue(state, reason)
                        return state, reason
                    if pd.notna(rt) and rt > self.latency_threshold_ms:
                        state, reason = "latency_issue", f"High latency detected: {rt:.2f} ms."
                        self._log_issue(state, reason)
                        return state, reason

            return "no_failure", "No issues detected."

        except (FileNotFoundError, pd.errors.EmptyDataError):
            return "no_failure", "Log or data file not found or empty."
        except Exception as e:
            return "no_failure", f"Error in IssueDetector: {e}"
