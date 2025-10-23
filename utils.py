# import pandas as pd
# import random
# import time
# import datetime
# import subprocess
# import os
# import shutil

# def simulate_data_change(dataset_path, force_anomaly=False):
#     """Creates a backup and appends new data, with a more impactful anomaly simulation."""
#     print(f"\nSimulating change for '{dataset_path}'...")
#     try:
#         if not os.path.exists(dataset_path):
#             raise FileNotFoundError(f"Dataset '{dataset_path}' not found. Please create it first.")

#         shutil.copyfile(dataset_path, f"{dataset_path}.bak")
#         print(f"  -> Created backup: {dataset_path}.bak")

#         df = pd.read_csv(dataset_path)

#         if "student_scores" in dataset_path:
#             # Add multiple low-score rows to guarantee the average drops below the threshold.
#             if force_anomaly:
#                 print("  -> Forcing a significant student score anomaly...")
#                 new_rows = []
#                 for _ in range(5): # Add 5 bad records
#                     new_rows.append({
#                         'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d'),
#                         'name': random.choice(['Alice', 'Bob', 'Charlie', 'David']),
#                         'subject': random.choice(['Math', 'Science', 'History', 'English']),
#                         'score': random.randint(10, 20) # Very low scores
#                     })
#                 df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
#             else:
#                 new_row = {
#                     'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d'),
#                     'name': random.choice(['Alice', 'Bob', 'Charlie', 'David']),
#                     'subject': random.choice(['Math', 'Science', 'History', 'English']),
#                     'score': random.randint(50, 100)
#                 }
#                 df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
#                 print("  -> Added a new student score record.")

#         elif "patient_health" in dataset_path:
#             # Also make the health anomaly more impactful
#             if force_anomaly:
#                 print("  -> Forcing a significant patient health anomaly...")
#                 hr, o2 = 150, 90
#             else:
#                 hr, o2 = random.randint(60, 100), random.randint(96, 100)
            
#             new_row = {
#                 'timestamp': pd.Timestamp.now(),
#                 'heart_rate': hr,
#                 'blood_pressure': f"{random.randint(110,140)}/{random.randint(70,90)}",
#                 'oxygen_level': o2
#             }
#             df = pd.concat([df, pd.DataFrame(new_row)], ignore_index=True)
#             print(f"  -> Added new patient health record. {'(ANOMALY FORCED)' if force_anomaly else ''}")

#         df.to_csv(dataset_path, index=False)
#         print(f"  -> Saved new data to '{dataset_path}'.")

#     except Exception as e:
#         print(f"Error simulating data change: {e}")


# def trigger_dashboard_deployment(timeout=15, should_fail=False, failure_type=None):
#     """
#     Starts the Streamlit dashboard as a subprocess.
#     If should_fail is True, it simulates a specific failure type ('crash' or 'latency').
#     """
#     print("Triggering dashboard deployment...")
    
#     # Only simulate a crash or latency if the fail_type is explicitly provided.
#     # Do NOT automatically fail just because force_anomaly is True.
#     if should_fail and failure_type:
#         if failure_type == 'crash':
#             print("  -> SIMULATING DEPLOYMENT FAILURE (CRASH).")
#             time.sleep(1.5)
#             return "failure", 2000
#         elif failure_type == 'latency':
#             print("  -> SIMULATING DEPLOYMENT SUCCESS (HIGH LATENCY).")
#             slow_time = timeout + 5
#             time.sleep(slow_time)
#             return "success", slow_time * 1000

#     # This is the default path for all deployments, including anomaly tests.
#     status, process = "failure", None
#     start_time = time.time()
#     try:
#         command = ["streamlit", "run", "app_dashboard.py", "--server.runOnSave", "false"]
#         process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#         time.sleep(timeout)
#         if process.poll() is None:
#             status = "success"
#         else:
#             status = "failure" # The app crashed (likely due to the bad data anomaly)
#     finally:
#         if process and process.poll() is None:
#             process.terminate()
#             process.wait(timeout=5)
#     end_time = time.time()
#     return status, (end_time - start_time) * 1000

















import pandas as pd
import random
import time
import datetime
import subprocess
import os
import shutil

def simulate_data_change(dataset_path, force_anomaly=False):
    """Creates a backup and appends new data, with a more impactful anomaly simulation."""
    print(f"\nSimulating change for '{dataset_path}'...")
    try:
        if not os.path.exists(dataset_path):
            raise FileNotFoundError(f"Dataset '{dataset_path}' not found. Please create it first.")

        shutil.copyfile(dataset_path, f"{dataset_path}.bak")
        print(f"  -> Created backup: {dataset_path}.bak")

        df = pd.read_csv(dataset_path)

        if "student_scores" in dataset_path:
            # Add multiple low-score rows to guarantee the average drops below the threshold.
            if force_anomaly:
                print("  -> Forcing a significant student score anomaly...")
                new_rows = []
                for _ in range(5): # Add 5 bad records
                    new_rows.append({
                        'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d'),
                        'name': random.choice(['Alice', 'Bob', 'Charlie', 'David']),
                        'subject': random.choice(['Math', 'Science', 'History', 'English']),
                        'score': random.randint(10, 20) # Very low scores
                    })
                df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
            else:
                new_row = {
                    'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d'),
                    'name': random.choice(['Alice', 'Bob', 'Charlie', 'David']),
                    'subject': random.choice(['Math', 'Science', 'History', 'English']),
                    'score': random.randint(50, 100)
                }
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                print("  -> Added a new student score record.")

        elif "patient_health" in dataset_path:
            # Also make the health anomaly more impactful
            if force_anomaly:
                print("  -> Forcing a significant patient health anomaly...")
                hr, o2 = 150, 90
            else:
                hr, o2 = random.randint(60, 100), random.randint(96, 100)
            
            new_row = {
                'timestamp': pd.Timestamp.now(),
                'heart_rate': hr,
                'blood_pressure': f"{random.randint(110,140)}/{random.randint(70,90)}",
                'oxygen_level': o2
            }
            df = pd.concat([df, pd.DataFrame(new_row)], ignore_index=True)
            print(f"  -> Added new patient health record. {'(ANOMALY FORCED)' if force_anomaly else ''}")

        df.to_csv(dataset_path, index=False)
        print(f"  -> Saved new data to '{dataset_path}'.")

    except Exception as e:
        print(f"Error simulating data change: {e}")


def trigger_dashboard_deployment(timeout=15, should_fail=False, failure_type=None):
    """
    Starts the Streamlit dashboard as a subprocess.
    If should_fail is True, it simulates a specific failure type ('crash' or 'latency').
    """
    print("Triggering dashboard deployment...")
    
    # Only simulate a crash or latency if the fail_type is explicitly provided.
    # Do NOT automatically fail just because force_anomaly is True.
    if should_fail and failure_type:
        if failure_type == 'crash':
            print("  -> SIMULATING DEPLOYMENT FAILURE (CRASH).")
            time.sleep(1.5)
            return "failure", 2000
        elif failure_type == 'latency':
            print("  -> SIMULATING DEPLOYMENT SUCCESS (HIGH LATENCY).")
            slow_time = timeout + 5
            time.sleep(slow_time)
            return "success", slow_time * 1000

    # This is the default path for all deployments, including anomaly tests.
    status, process = "failure", None
    start_time = time.time()
    try:
        command = ["streamlit", "run", "app_dashboard.py", "--server.runOnSave", "false"]
        process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(timeout)
        if process.poll() is None:
            status = "success"
        else:
            status = "failure" # The app crashed (likely due to the bad data anomaly)
    finally:
        if process and process.poll() is None:
            process.terminate()
            process.wait(timeout=5)
    end_time = time.time()
    return status, (end_time - start_time) * 1000

