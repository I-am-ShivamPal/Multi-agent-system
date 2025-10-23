import argparse
import os
import csv
import datetime
from agents.deploy_agent import DeployAgent
from agents.issue_detector import IssueDetector
from agents.uptime_monitor import UptimeMonitor
from agents.auto_heal_agent import AutoHealAgent
from rl.rl_trainer import RLTrainer 
from utils import simulate_data_change, trigger_dashboard_deployment

def get_user_feedback_from_terminal(state, action, outcome):
    """Prompts the user for feedback directly in the terminal."""
    print("\n" + "="*30)
    print("✍️ USER FEEDBACK REQUIRED:")
    print(f"  - Problem Detected: {state}")
    print(f"  - Agent's Chosen Action: {action}")
    print(f"  - System Outcome: {outcome}")
    
    while True:
        response = input("Do you accept this action as a good solution for this problem? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            print(" -> Feedback recorded: ACCEPTED.")
            return 'accepted'
        elif response in ['n', 'no']:
            print(" -> Feedback recorded: REJECTED.")
            return 'rejected'
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")

def log_user_feedback(log_file, state, action, outcome, feedback):
    """Logs the user's raw feedback to a permanent history file."""
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    header = ["timestamp", "state", "action", "system_outcome", "user_feedback"]
    
    file_exists = os.path.exists(log_file)
    
    timestamp = datetime.datetime.now().isoformat()
    with open(log_file, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists or f.tell() == 0:
            writer.writerow(header)
        writer.writerow([timestamp, state, action, outcome, feedback])
    print(f" -> User feedback permanently stored in {log_file}")

# --- Main Simulation Loop ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CI/CD Simulation with Modular Agents")
    parser.add_argument("--dataset", type=str, default="dataset/student_scores.csv")
    parser.add_argument("--fail-type", type=str, choices=['crash', 'latency'])
    parser.add_argument("--force-anomaly", action="store_true")
    parser.add_argument("--planner", type=str, choices=['random', 'rl'], default='random')
    parser.add_argument("--train", action="store_true")
    args = parser.parse_args()

    # --- File Path Definitions ---
    LOG_DIR = "logs"
    DEPLOYMENT_LOG_FILE = os.path.join(LOG_DIR, "deployment_log.csv")
    UPTIME_LOG_FILE = os.path.join(LOG_DIR, "uptime_log.csv")
    HEALING_LOG_FILE = os.path.join(LOG_DIR, "healing_log.csv")
    RL_LOG_FILE = os.path.join(LOG_DIR, "rl_log.csv")
    PERFORMANCE_LOG_FILE = os.path.join(LOG_DIR, "rl_performance_log.csv")
    ISSUE_LOG_FILE = os.path.join(LOG_DIR, "issue_log.csv")
    # --- THIS IS THE FIX (Part 1) ---
    USER_FEEDBACK_LOG_FILE = os.path.join(LOG_DIR, "user_feedback_log.csv") # New file for permanent storage

    # --- Agent Initialization ---
    deploy_agent = DeployAgent(log_file=DEPLOYMENT_LOG_FILE)
    issue_detector = IssueDetector(log_file=DEPLOYMENT_LOG_FILE, data_file=args.dataset, issue_log_file=ISSUE_LOG_FILE)
    uptime_monitor = UptimeMonitor(timeline_file=UPTIME_LOG_FILE)
    
    planner = AutoHealAgent(healing_log_file=HEALING_LOG_FILE)
    trainer = None
    if args.planner == 'rl':
        trainer = RLTrainer(rl_log_file=RL_LOG_FILE, performance_log_file=PERFORMANCE_LOG_FILE, train_mode=args.train)
        print("\n--- Using RL Trainer for action selection ---")

    # --- Simulation Logic ---
    simulate_data_change(args.dataset, force_anomaly=args.force_anomaly)
    
    should_fail = args.fail_type is not None or args.force_anomaly
    status, time_ms = trigger_dashboard_deployment(should_fail=should_fail, failure_type=args.fail_type)
    deploy_agent.log_deployment(args.dataset, status, time_ms)

    failure_state, reason = issue_detector.detect_failure_type()
    
    if failure_state != "no_failure":
        system_status = uptime_monitor.last_status
        full_state = f"{failure_state}_{system_status}"
        
        uptime_monitor.update_status("DOWN", reason)
        
        if trainer:
            chosen_action = trainer.choose_action(full_state)
            heal_status, heal_time, heal_type, _ = planner.execute_action(chosen_action, args.dataset)
        else:
            heal_status, heal_time, heal_type, chosen_action = planner.attempt_healing(full_state, args.dataset)
        
        if trainer:
            base_reward = 1 if heal_status == 'success' else -1
            user_feedback = get_user_feedback_from_terminal(full_state, chosen_action, heal_status)
            
            # --- THIS IS THE FIX (Part 2) ---
            # Log the raw user feedback to its own permanent file
            log_user_feedback(USER_FEEDBACK_LOG_FILE, full_state, chosen_action, heal_status, user_feedback)
            
            # The agent learns from the feedback
            trainer.learn(full_state, chosen_action, base_reward, user_feedback)
        
        deploy_agent.log_deployment(args.dataset, heal_status, heal_time, action_type=heal_type)

        if heal_status == 'success':
            uptime_monitor.update_status("UP", f"Recovery successful via {heal_type}")
        else:
            print("\n--- Healing attempt failed. The service remains down. ---")
    else:
        uptime_monitor.update_status("UP", "Successful deployment")

    if trainer:
        trainer.save_q_table()
        
    print("\nCI/CD simulation finished.")

