# import argparse
# import os
# import csv
# import datetime
# from agents.issue_detector import IssueDetector
# from agents.uptime_monitor import UptimeMonitor
# from agents.auto_heal_agent import AutoHealAgent
# # from agents.rl_optimizer import RLOptimizer
# from feedback.feedback_handler import FeedbackHandler
# from rl.rl_trainer import RLOptimizer
# from utils import simulate_data_change, trigger_dashboard_deployment

# def log_master_event(log_file, event_type, dataset, status, details=""):
#     """Centralized master event logger."""
#     os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
#     if not os.path.exists(log_file):
#         with open(log_file, 'w', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow(["timestamp", "event_type", "dataset", "status", "details"])

#     timestamp = datetime.datetime.now().isoformat()
#     with open(log_file, 'a', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow([timestamp, event_type, dataset, status, details])
    
#     print(f"📋 MASTER LOG: Event='{event_type}', Status='{status}', Details='{details}'")

# # --- MAIN SIMULATION LOOP ---
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="CI/CD Master Orchestrator")
#     parser.add_argument("--dataset", type=str, default="dataset/student_scores.csv")
#     parser.add_argument("--fail-type", type=str, choices=['crash', 'latency'])
#     parser.add_argument("--force-anomaly", action="store_true")
#     parser.add_argument("--planner", type=str, choices=['random', 'rl'], default='random')
#     parser.add_argument("--train", action="store_true")
#     args = parser.parse_args()

#     # --- File Paths ---
#     LOG_DIR = "logs"
#     os.makedirs(LOG_DIR, exist_ok=True)

#     MASTER_LOG_FILE = os.path.join(LOG_DIR, "master_log.csv")
#     DEPLOYMENT_LOG_FILE = os.path.join(LOG_DIR, "deployment_log.csv")
#     HEALING_LOG_FILE = os.path.join(LOG_DIR, "healing_log.csv")
#     RL_LOG_FILE = os.path.join(LOG_DIR, "rl_log.csv")
#     FEEDBACK_FILE = os.path.join(LOG_DIR, "user_feedback.csv")
#     UPTIME_LOG_FILE = os.path.join(LOG_DIR, "uptime_log.csv")
#     ISSUE_LOG_FILE = os.path.join(LOG_DIR, "issue_log.csv")
    
    
#     # //////////////////////////////////////////////////////////////////////////////////////////////////
#     feedback_handler = FeedbackHandler(FEEDBACK_FILE)

#     # --- Agent Initialization ---
#     issue_detector = IssueDetector(log_file=DEPLOYMENT_LOG_FILE, data_file=args.dataset, issue_log_file=ISSUE_LOG_FILE)
#     uptime_monitor = UptimeMonitor(timeline_file=UPTIME_LOG_FILE)

#     if args.planner == 'rl':
#         planner = RLOptimizer(
#             healing_log_file=HEALING_LOG_FILE,
#             rl_log_file=RL_LOG_FILE,
#             feedback_file=FEEDBACK_FILE,
#             train_mode=args.train
#         )
#         print("\n🤖 === USING RL OPTIMIZER ===")
#         if args.train:
#             print("🎓 === TRAINING MODE ACTIVE ===")
#     else:
#         planner = AutoHealAgent(healing_log_file=HEALING_LOG_FILE)
#         print("\n🎲 === USING RANDOM AUTO-HEAL AGENT ===")
#         if args.train:
#             print("⚠️  WARNING: --train flag ignored (only works with --planner rl)")

#     print(f"\n{'='*60}")
#     print(f"🚀 Starting Simulation for {os.path.basename(args.dataset)}")
#     print(f"   Planner: {args.planner.upper()}")
#     print(f"   Force Anomaly: {args.force_anomaly}")
#     print(f"   Training Mode: {args.train}")
#     print(f"{'='*60}\n")

#     # 1️⃣ Simulate a data change
#     simulate_data_change(args.dataset, force_anomaly=args.force_anomaly)

#     # 🔥 KEY FIX: Check for data anomalies BEFORE deploying
#     print("\n" + "="*60)
#     print("🔍 STEP 1: PRE-DEPLOYMENT DATA QUALITY CHECK")
#     print("="*60)
#     pre_check_state, pre_check_reason = issue_detector.check_data_quality_only()
#     print(f"Result: {pre_check_state}")
#     print(f"Reason: {pre_check_reason}")
    
#     if pre_check_state != "no_failure":
#         print(f"\n🚨 DATA QUALITY ISSUE DETECTED: {pre_check_state}")
#         print(f"   Reason: {pre_check_reason}")
#         log_master_event(MASTER_LOG_FILE, "Data Quality Check", args.dataset, pre_check_state, pre_check_reason)
#         uptime_monitor.update_status("DOWN", pre_check_reason)
        
#         print(f"\n{'='*60}")
#         print(f"🔧 ATTEMPTING TO HEAL DATA ANOMALY: {pre_check_state}")
#         print(f"{'='*60}")
        
#         # Attempt healing BEFORE deployment
#         heal_status, heal_time, heal_type, chosen_action = planner.attempt_healing(pre_check_state, args.dataset)
#         log_master_event(MASTER_LOG_FILE, f"Pre-Deploy Healing ({chosen_action})", args.dataset, heal_status, f"{heal_time:.2f} ms")
        
#         # RL Learning for data anomalies
#         # if args.planner == 'rl':
#         #     reward = 1 if heal_status == "success" else -1
#         #     print(f"\n{'='*60}")
#         #     print(f"🧠 RL LEARNING SESSION")
#         #     print(f"{'='*60}")
#         #     print(f"   State: '{pre_check_state}'")
#         #     print(f"   Action: '{chosen_action}'")
#         #     print(f"   Outcome: '{heal_status}'")
#         #     print(f"   Reward: {reward}")
#         #     print(f"{'='*60}")
#         #     planner.update_q_table(pre_check_state, chosen_action, reward)
#         if args.planner == 'rl':
#     # === User Feedback Integration ===
#             feedback_value = input("\nWas the auto-heal successful? (yes/no/neutral): ").strip().lower()
#             if feedback_value in ['yes', 'y']:
#                 fb_val = "positive"
#             elif feedback_value in ['no', 'n']:
#                 fb_val = "negative"
#             else:
#                 fb_val = "neutral"

#             reward = feedback_handler.log_feedback(pre_check_state, chosen_action, heal_status, "user", fb_val)
#             planner.update_q_table(pre_check_state, chosen_action, reward)

        
        
        
        
        
        
#         if heal_status != "success":
#             print("\n❌ Data quality issue unresolved. Skipping deployment.")
#             if args.planner == 'rl':
#                 planner.save_q_table()
#                 print(f"\n💾 Q-table saved to {RL_LOG_FILE}")
#                 # Print current Q-table
#                 print("\n📊 Current Q-Table State:")
#                 print(planner.q_table)
#             print("\n--- Simulation Finished ---")
#             exit(0)
#         else:
#             print("\n✅ Data quality restored. Proceeding with deployment...")
#     else:
#         print("✅ Data quality check passed - no anomalies detected")

#     # 2️⃣ Trigger dashboard deployment
#     print(f"\n{'='*60}")
#     print("🚀 STEP 2: TRIGGERING DEPLOYMENT")
#     print(f"{'='*60}")
    
#     should_fail = args.fail_type is not None
#     status, time_ms = trigger_dashboard_deployment(should_fail=should_fail, failure_type=args.fail_type)

#     # Log deployment result
#     with open(DEPLOYMENT_LOG_FILE, 'a', newline='') as f:
#         writer = csv.writer(f)
#         if f.tell() == 0:
#             writer.writerow(["timestamp", "dataset", "status", "response_time_ms"])
#         writer.writerow([datetime.datetime.now().isoformat(), args.dataset, status, f"{time_ms:.2f}"])
#     log_master_event(MASTER_LOG_FILE, "Deployment", args.dataset, status, f"Response time: {time_ms:.2f} ms")
    
#     print(f"Deployment Status: {status}")
#     print(f"Response Time: {time_ms:.2f} ms")

#     # 3️⃣ Detect Post-Deployment Issues (latency, deployment failures)
#     print(f"\n{'='*60}")
#     print("🔍 STEP 3: POST-DEPLOYMENT ISSUE CHECK")
#     print(f"{'='*60}")
    
#     failure_state, reason = issue_detector.check_deployment_issues_only()
#     print(f"Result: {failure_state}")
#     print(f"Reason: {reason}")
    
#     if failure_state != "no_failure":
#         print(f"\n🚨 POST-DEPLOYMENT ISSUE: {failure_state} - {reason}")
#         log_master_event(MASTER_LOG_FILE, "Post-Deploy Issue", args.dataset, failure_state, reason)
#         uptime_monitor.update_status("DOWN", reason)

#         # Attempt healing
#         heal_status, heal_time, heal_type, chosen_action = planner.attempt_healing(failure_state, args.dataset)
#         log_master_event(MASTER_LOG_FILE, f"Healing ({chosen_action})", args.dataset, heal_status, f"{heal_time:.2f} ms")

#         # # RL Learning
#         # if args.planner == 'rl':
#         #     reward = 1 if heal_status == "success" else -1
#         #     print(f"\n{'='*60}")
#         #     print(f"🧠 RL LEARNING SESSION")
#         #     print(f"{'='*60}")
#         #     print(f"   State: '{failure_state}'")
#         #     print(f"   Action: '{chosen_action}'")
#         #     print(f"   Outcome: '{heal_status}'")
#         #     print(f"   Reward: {reward}")
#         #     print(f"{'='*60}")
#         #     planner.update_q_table(failure_state, chosen_action, reward)
#         if args.planner == 'rl':
#             # === User Feedback Integration ===
#             feedback_value = input("\nWas the auto-heal successful? (yes/no/neutral): ").strip().lower()
#             if feedback_value in ['yes', 'y']:
#                 fb_val = "positive"
#             elif feedback_value in ['no', 'n']:
#                 fb_val = "negative"
#             else:
#                 fb_val = "neutral"

#             reward = feedback_handler.log_feedback(failure_state, chosen_action, heal_status, "user", fb_val)
#             planner.update_q_table(failure_state, chosen_action, reward)
#             planner.save_q_table()
#             print(f"💾 Q-table updated and re-saved after user feedback.")





#         if heal_status == "success":
#             uptime_monitor.update_status("UP", f"Recovery successful via {heal_type}")
#             print("\n✅ Healing successful. System recovered.")
#         else:
#             print("\n❌ Healing failed. System remains down.")
#     else:
#         uptime_monitor.update_status("UP", "Deployment succeeded with no issues.")
#         print("✅ No post-deployment issues detected")

#     # 4️⃣ Save RL Q-table
#     if args.planner == 'rl':
#         print(f"\n{'='*60}")
#         print("💾 SAVING RL Q-TABLE")
#         print(f"{'='*60}")
#         planner.save_q_table()
#         print(f"Saved to: {RL_LOG_FILE}")
#         print("\n📊 Final Q-Table State:")
#         print(planner.q_table)
#         print(f"{'='*60}")

#     print("\n✅ === SIMULATION FINISHED ===\n")







# import argparse
# import os
# from agents.deploy_agent import DeployAgent
# from agents.issue_detector import IssueDetector
# from agents.uptime_monitor import UptimeMonitor
# from agents.auto_heal_agent import AutoHealAgent
# from rl.rl_trainer import RLTrainer
# from utils import simulate_data_change, trigger_dashboard_deployment

# def get_user_feedback_from_terminal(state, action, outcome):
#     """Prompts the user for feedback directly in the terminal."""
#     print("\n" + "="*30)
#     print("✍️ USER FEEDBACK REQUIRED:")
#     print(f"  - Problem Detected: {state}")
#     print(f"  - Agent's Chosen Action: {action}")
#     print(f"  - System Outcome: {outcome}")
    
#     while True:
#         response = input("Do you accept this action as a good solution for this problem? (y/n): ").lower().strip()
#         if response in ['y', 'yes']:
#             print(" -> Feedback recorded: ACCEPTED.")
#             return 'accepted'
#         elif response in ['n', 'no']:
#             print(" -> Feedback recorded: REJECTED.")
#             return 'rejected'
#         else:
#             print("Invalid input. Please enter 'y' for yes or 'n' for no.")

# # --- Main Simulation Loop ---
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="CI/CD Simulation with Modular Agents")
#     parser.add_argument("--dataset", type=str, default="dataset/student_scores.csv")
#     parser.add_argument("--fail-type", type=str, choices=['crash', 'latency'])
#     parser.add_argument("--force-anomaly", action="store_true")
#     parser.add_argument("--planner", type=str, choices=['random', 'rl'], default='random')
#     parser.add_argument("--train", action="store_true")
#     args = parser.parse_args()

#     # --- File Path Definitions ---
#     LOG_DIR = "logs"
#     DEPLOYMENT_LOG_FILE = os.path.join(LOG_DIR, "deployment_log.csv")
#     UPTIME_LOG_FILE = os.path.join(LOG_DIR, "uptime_log.csv")
#     HEALING_LOG_FILE = os.path.join(LOG_DIR, "healing_log.csv")
#     RL_LOG_FILE = os.path.join(LOG_DIR, "rl_log.csv")
#     PERFORMANCE_LOG_FILE = os.path.join(LOG_DIR, "rl_performance_log.csv")
#     ISSUE_LOG_FILE = os.path.join(LOG_DIR, "issue_log.csv")

#     # --- Agent Initialization ---
#     deploy_agent = DeployAgent(log_file=DEPLOYMENT_LOG_FILE)
#     issue_detector = IssueDetector(log_file=DEPLOYMENT_LOG_FILE, data_file=args.dataset, issue_log_file=ISSUE_LOG_FILE)
#     uptime_monitor = UptimeMonitor(timeline_file=UPTIME_LOG_FILE)
    
#     planner = AutoHealAgent(healing_log_file=HEALING_LOG_FILE)
#     trainer = None
#     if args.planner == 'rl':
#         trainer = RLTrainer(rl_log_file=RL_LOG_FILE, performance_log_file=PERFORMANCE_LOG_FILE, train_mode=args.train)
#         print("\n--- Using RL Trainer for action selection ---")
#         if args.train: print("--- TRAINING MODE ACTIVE ---")
#     else:
#         print("\n--- Using Random Auto-Heal Agent ---")

#     # --- Simulation Logic ---
#     simulate_data_change(args.dataset, force_anomaly=args.force_anomaly)
    
#     should_fail = args.fail_type is not None or args.force_anomaly
#     status, time_ms = trigger_dashboard_deployment(should_fail=should_fail, failure_type=args.fail_type)
#     deploy_agent.log_deployment(args.dataset, status, time_ms)

#     failure_state, reason = issue_detector.detect_failure_type()
    
#     if failure_state != "no_failure":
#         system_status = uptime_monitor.last_status
#         full_state = f"{failure_state}_{system_status}"
        
#         uptime_monitor.update_status("DOWN", reason)
        
#         if trainer:
#             chosen_action = trainer.choose_action(full_state)
#             heal_status, heal_time, heal_type, _ = planner.execute_action(chosen_action, args.dataset)
#         else:
#             heal_status, heal_time, heal_type, chosen_action = planner.attempt_healing(full_state, args.dataset)
        
#         if trainer:
#             base_reward = 1 if heal_status == 'success' else -1
#             user_feedback = get_user_feedback_from_terminal(full_state, chosen_action, heal_status)
#             trainer.learn(full_state, chosen_action, base_reward, user_feedback)
        
#         deploy_agent.log_deployment(args.dataset, heal_status, heal_time, action_type=heal_type)

#         if heal_status == 'success':
#             uptime_monitor.update_status("UP", f"Recovery successful via {heal_type}")
#         else:
#             print("\n--- Healing attempt failed. The service remains down. ---")
#     else:
#         uptime_monitor.update_status("UP", "Successful deployment")

#     if trainer:
#         trainer.save_q_table()
        
#     print("\nCI/CD simulation finished.")





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

