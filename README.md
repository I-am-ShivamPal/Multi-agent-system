# Self-Healing CI/CD Pipeline Simulation

This project simulates a self-healing CI/CD pipeline for a data dashboard using a multi-agent system. The system automatically deploys changes, detects a variety of failures (crashes, latency, data anomalies), and uses an intelligent agent to perform recovery actions.

The core of the project is an RL Optimizer Agent (RLTrainer) that uses Q-learning to learn the most effective healing strategy for different problems using Q-learning, guided by a terminal-based feedback loop, allowing a human supervisor to "accept" or "reject" its automated decisions, dynamically adjusting the rewards and shaping its policy.

This repository is structured for a clean handover to UI/UX and integration teams.

# 🏛️ Project Architecture

The system is designed with a clean separation of concerns. A central main.py orchestrator controls the simulation, while modular agents, trainers, and dashboards live in their own packages. Communication and state are managed through a series of structured log files in the /logs directory.

/
├── agents/
│   ├── __init__.py
│   ├── deploy_agent.py         # Logs deployment attempts
│   ├── issue_detector.py       # Detects failures (crash, latency, anomaly)
│   ├── uptime_monitor.py       # Logs UP/DOWN status
│   └── auto_heal_agent.py      # Executes the healing actions (the "engine")
│
├── rl/
│   ├── __init__.py
│   └── rl_trainer.py           # The "brain" (Q-learning, policy, learning logic)
│
├── feedback/
│   ├── __init__.py
│   └── feedback_handler.py     # Handles the terminal-based user feedback prompt
│
├── dashboard/
│   ├── __init__.py
│   └── control_board.py        # The Streamlit monitoring dashboard
│
├── dataset/
│   ├── student_scores.csv      # Sample data
│   └── patient_health.csv      # Sample data
│
├── logs/
│   ├── (all log files are generated here)
│
├── main.py                     # The main script to run the simulation
├── utils.py                    # Shared functions (simulate data change, trigger deploy)
├── dashboard.py                # The dummy app that is "deployed"
├── mcp_stub.py                 # Placeholder for JSON-based message passing
├── README.md                   # This file
└── requirements.txt            # Project dependencies


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
