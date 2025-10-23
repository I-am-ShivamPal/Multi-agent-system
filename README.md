# Self-Healing CI/CD Pipeline Simulation

This project simulates a self-healing CI/CD pipeline for a data dashboard using a multi-agent system. The system automatically deploys changes, detects a variety of failures (crashes, latency, data anomalies), and uses an intelligent agent to perform recovery actions.

The core of the project is an RL Optimizer Agent (RLTrainer) that uses Q-learning to learn the most effective healing strategy for different problems using Q-learning, guided by a terminal-based feedback loop, allowing a human supervisor to "accept" or "reject" its automated decisions, dynamically adjusting the rewards and shaping its policy.

This repository is structured for a clean handover to UI/UX and integration teams.

# 🏛️ Project Architecture

The system is designed with a clean separation of concerns. A central main.py orchestrator controls the simulation, while modular agents, trainers, and dashboards live in their own packages. Communication and state are managed through a series of structured log files in the /logs directory.

### 1. The Root Folder (The Factory Floor)
This is the main control center where you start the simulation and find the core pieces.

* `main.py`: This is the **Factory Manager**. You run this one file to start the entire simulation. It tells all the agents what to do and in what order.
* `utils.py`: This is the **Toolbox**. It holds shared tools (like `simulate_data_change` or `trigger_dashboard_deployment`) that any agent can use to do its job.
* `dashboard.py`: This is the **Product** being built. It's the dummy Streamlit dashboard that the factory is trying to deploy.
* `mcp_stub.py`: This is a **Note for the Next Team** (for Ritesh). It's a placeholder that shows how your agents will send JSON messages.
* `README.md`: The **Instruction Manual** for the whole project.
* `requirements.txt`: The **Parts List** of all the software needed to run the factory.

### 2. The `/agents/` Folder (The Workers)
This folder is a department of specialized workers. Each one has a very specific job.

* `deploy_agent.py`: The **Clerk**. Its *only* job is to write down every deployment (success or fail) into the `deployment_log.csv`.
* `issue_detector.py`: The **Inspector**. Its job is to look at the data and logs to find out *what* went wrong (e.g., a crash, a data anomaly).
* `uptime_monitor.py`: The **Status Tracker**. It keeps a simple log of whether the system is "UP" or "DOWN."
* `auto_heal_agent.py`: The **Mechanic**. This agent has the "hands" and knows *how* to perform the actual fixes (retry, rollback, etc.).

### 3. The `/rl/` Folder (The Brain)
This folder contains the project's intelligence.

* `rl_trainer.py`: The **Smart Agent** or "Brain." It *decides* which fix to use by looking at its past experience (the Q-Table). It then tells the "Mechanic" (`auto_heal_agent`) what to do.

### 4. The `/feedback/` Folder (The Supervisor's Office)
This is where you, the human, come in.

* `feedback_handler.py`: This is your **Assistant**. Its job is to pause the simulation and ask for your expert opinion ("Accept" or "Reject") right in the terminal.

### 5. The `/dashboard/` Folder (The Control Room)
* `control_board.py`: This is your **Monitor**. It's the main Streamlit dashboard you run to *see* all the logs, watch the agent's performance, and check the system's uptime.

### 6. The `/dataset/` and `/logs/` Folders
* `dataset/`: This is the **Raw Material** (your health and student data files).
* `logs/`: This is the **Filing Cabinet** where all the agents store their reports (all the `.csv` log files).


(Note: The file structure diagram has been updated to reflect the final project, including rl_optimizer_agent.py which seems to be a legacy file, and the correct dashboard name dashboard.py.)

# **⚙️ Environment Setup**

Prerequisites

Python 3.8+

pip and venv (standard Python libraries)

Installation Guide

Clone the Repository: https://github.com/I-am-ShivamPal/Multi-agent-system

git clone 
cd Multi-agent-system


Create a Virtual Environment:
It is highly recommended to use a virtual environment to manage project dependencies.


Install Dependencies:
This project requires several Python packages. A requirements.txt file is provided for easy installation.

pip install -r requirements.txt


# **🚀 How to Run the Project (Demo Guide)**

This project has two main parts that run at the same time in separate terminals: the Live Dashboard (for monitoring) and the Simulation Runner (for running tests).

Terminal 1: Start the Monitoring Dashboard

First, launch the Streamlit " Dasshboard" to monitor your system.

streamlit run dashboard/dashboard.py


This will open the dashboard in your web browser (usually at http://localhost:8501). Keep this terminal open.

Terminal 2: Run the Simulation

In a second, separate terminal, you will run main.py to execute the simulation. The dashboard will update in near-real-time.

1. Basic Simulation (Random Agent)

This will run a simple simulation using the "random" AutoHealAgent.

Run on Student Scores (default):

python main.py


Run on Patient Health:

python main.py --dataset dataset/patient_health.csv


2. Training the RL Agent (Main Workflow)

This is the core of the project. Here, you will use the --planner rl flag to activate the RLTrainer and use failure flags to teach it.

Step 1: Simulate a Failure
Run a command to simulate a specific type of failure.

To simulate a crash:

python main.py --planner rl --fail-type crash


To simulate a latency (slowness) issue:

python main.py --planner rl --fail-type latency


To simulate a data anomaly (bad student score):

python main.py --planner rl --force-anomaly --dataset dataset/student_scores.csv


Step 2: Provide Terminal Feedback
The simulation will pause and ask for your expert feedback in the terminal.

✍️ USER FEEDBACK REQUIRED:
  - Problem Detected: deployment_failure_DOWN
  - Agent's Chosen Action: retry_deployment
  - System Outcome: failure
Do you accept this action as a good solution for this problem? (y/n):


Type y (yes) to Accept the agent's strategy (e.g., retrying a crash is a good idea, even if it failed). The agent gets a positive reward.

Type n (no) to Reject the strategy (e.g., retrying a data anomaly is a bad idea). The agent will be penalized with a -1 reward.

Step 3: See the Results
After you give feedback, the simulation will finish. Go back to your dashboard in the browser. The "Agent Intelligence" tab will be updated, showing new values in the RL Policy Q-Table as the agent learns from your feedback.
