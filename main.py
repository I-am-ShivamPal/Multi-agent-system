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
from feedback.feedback_handler import get_user_feedback_from_terminal, log_user_feedback
from config import THRESHOLDS # This line imports the thresholds

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
    USER_FEEDBACK_LOG_FILE = os.path.join(LOG_DIR, "user_feedback_log.csv")

    # --- Agent Initialization ---
    deploy_agent = DeployAgent(log_file=DEPLOYMENT_LOG_FILE)

    # --- THIS IS THE FIX ---
    # The configuration dictionary is correctly passed to the IssueDetector.
    issue_detector = IssueDetector(
        log_file=DEPLOYMENT_LOG_FILE, 
        data_file=args.dataset, 
        issue_log_file=ISSUE_LOG_FILE,
        config=THRESHOLDS
    )
    # -------------------------
    
    uptime_monitor = UptimeMonitor(timeline_file=UPTIME_LOG_FILE)
    
    planner = AutoHealAgent(healing_log_file=HEALING_LOG_FILE) # This agent executes the actions
    trainer = None
    if args.planner == 'rl':
        trainer = RLTrainer(rl_log_file=RL_LOG_FILE, performance_log_file=PERFORMANCE_LOG_FILE, train_mode=args.train)
        print("\n--- Using RL Trainer for action selection ---")
    else:
        print("\n--- Using Random Auto-Heal Agent ---")

    # 1. Simulate a data change
    simulate_data_change(args.dataset, force_anomaly=args.force_anomaly)
    
    # 2. Trigger initial deployment
    should_fail = args.fail_type is not None or args.force_anomaly
    status, time_ms = trigger_dashboard_deployment(should_fail=should_fail, failure_type=args.fail_type)
    deploy_agent.log_deployment(args.dataset, status, time_ms)

    # 3. Detect Issues and Heal if Necessary
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
            log_user_feedback(USER_FEEDBACK_LOG_FILE, full_state, chosen_action, heal_status, user_feedback)
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

