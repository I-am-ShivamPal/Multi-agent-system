# import streamlit as st
# import pandas as pd
# import os
# import plotly.express as px
# import matplotlib.pyplot as plt
# import seaborn as sns

# # --- Page Configuration ---
# st.set_page_config(
#     page_title="CI/CD Simulation Dashboard",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # --- Data Loading (Robust Version) ---
# @st.cache_data(ttl=5)
# def load_data():
#     """Loads all data sources, handling file errors and parsing issues gracefully."""
#     data = {}
#     files = {
#         "deploy_log": "logs/deployment_log.csv",
#         "uptime": "logs/uptime_log.csv",
#         "healing_log": "logs/healing_log.csv",
#         "q_table": "logs/rl_log.csv",
#         "scores": "dataset/student_scores.csv",
#         "health": "dataset/patient_health.csv",
#         "feedback": "logs/user_feedback.csv",
#         "issue_log": "logs/issue_log.csv"
#     }
#     for key, filename in files.items():
#         if os.path.exists(filename):
#             try:
#                 if key == "q_table":
#                     data[key] = pd.read_csv(filename, index_col=0)
#                 else:
#                     data[key] = pd.read_csv(filename)
#             except (pd.errors.ParserError, pd.errors.EmptyDataError):
#                 st.error(f"Error parsing `{filename}`. The file may be corrupted. Please delete it and re-run the simulation.")
#                 data[key] = pd.DataFrame()
#         else:
#             data[key] = pd.DataFrame()
#     return data

# # --- Load and Preprocess Data ---
# data_frames = load_data()
# deploy_log_df = data_frames["deploy_log"]
# uptime_df = data_frames["uptime"]
# healing_log_df = data_frames["healing_log"]
# q_table_df = data_frames["q_table"]
# scores_df = data_frames["scores"]
# health_df = data_frames["health"]
# feedback_df = data_frames["feedback"]
# issue_log_df = data_frames["issue_log"]

# for df in [scores_df, health_df, deploy_log_df, uptime_df, healing_log_df, feedback_df, issue_log_df]:
#     if not df.empty and 'timestamp' in df.columns:
#         df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# # --- SIDEBAR ---
# st.sidebar.header("Dashboard Filters ⚙️")
# performance_view = st.sidebar.selectbox(
#     "Select Performance View:",
#     ["Student Scores", "Patient Health"]
# )

# # --- MAIN DASHBOARD UI ---
# st.title("🤖 CI/CD Agent Simulation Master Dashboard")
# if st.button("🔄 Refresh Data"):
#     st.rerun()

# tab1, tab2, tab3, tab4 = st.tabs([
#     "📊 Performance & Event Timeline",
#     "🧠 Agent Intelligence",
#     "🩺 System Health Summary",
#     "🗂️ Raw Data Logs"
# ])

# # =======================================================
# # TAB 1: PERFORMANCE & EVENTS
# # =======================================================
# with tab1:
#     st.header(f"{performance_view} Performance")
#     if performance_view == "Student Scores":
#         if not scores_df.empty and 'timestamp' in scores_df.columns:
#             df_to_plot = scores_df.copy()
#             avg_scores = df_to_plot.groupby(df_to_plot['timestamp'].dt.date)['score'].mean().reset_index()
#             fig = px.line(avg_scores, x='timestamp', y='score', markers=True,
#                           labels={'timestamp': 'Date', 'score': 'Average Score'}, template="plotly_dark")
#             fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False, title=None)
#             for _, row in deploy_log_df.iterrows():
#                 if pd.notna(row['timestamp']):
#                     fig.add_vline(x=str(row['timestamp'].date()), line_width=1.5, line_dash="dash",
#                                   line_color="green" if row['status'] == 'success' else "red")
#             st.plotly_chart(fig, use_container_width=True)
#         else:
#             st.warning("`dataset/student_scores.csv` is missing or invalid.")

#     elif performance_view == "Patient Health":
#         if not health_df.empty and 'timestamp' in health_df.columns:
#             df_to_plot = health_df.sort_values('timestamp').copy()
#             col1, col2 = st.columns(2)
#             with col1:
#                 st.subheader("Heart Rate")
#                 fig_hr = px.line(df_to_plot, x='timestamp', y='heart_rate', markers=True, template="plotly_dark")
#                 st.plotly_chart(fig_hr, use_container_width=True)
#             with col2:
#                 st.subheader("Oxygen Level")
#                 fig_o2 = px.line(df_to_plot, x='timestamp', y='oxygen_level', markers=True, template="plotly_dark")
#                 st.plotly_chart(fig_o2, use_container_width=True)
#         else:
#             st.warning("`dataset/patient_health.csv` is missing or invalid.")

#     st.header("Combined Event Timeline")
#     logs_to_combine = []
#     if not deploy_log_df.empty: logs_to_combine.append(deploy_log_df.rename(columns={'action_type': 'event_type'}))
#     if not uptime_df.empty: logs_to_combine.append(uptime_df.rename(columns={'status': 'event_type', 'event': 'details'}))
#     if not healing_log_df.empty: logs_to_combine.append(healing_log_df.rename(columns={'strategy': 'event_type'}))
#     if not issue_log_df.empty: logs_to_combine.append(issue_log_df.rename(columns={'failure_state': 'event_type', 'reason': 'details'}))

#     if logs_to_combine:
#         all_logs = pd.concat(logs_to_combine, ignore_index=True)
#         if 'timestamp' in all_logs.columns:
#             all_logs = all_logs.sort_values(by='timestamp', ascending=False)
#             display_cols = [col for col in ['timestamp', 'event_type', 'status', 'details', 'dataset_changed'] if col in all_logs.columns]
#             st.dataframe(all_logs[display_cols], use_container_width=True)
#     else:
#         st.warning("No log data available.")

# # =======================================================
# # TAB 2: AGENT INTELLIGENCE
# # =======================================================
# with tab2:
#     st.header("Healing Agent Performance")
#     if not healing_log_df.empty:
#         success_rate = (healing_log_df['status'] == 'success').sum() / len(healing_log_df) * 100
#         col1, col2 = st.columns(2)
#         with col1: st.metric("Total Healing Attempts", len(healing_log_df))
#         with col2: st.metric("Healing Success Rate", f"{success_rate:.1f}%")
#     else:
#         st.info("No healing actions logged yet.")

#     st.header("✍️ User Feedback on Last Healing Action")
    
#     show_feedback_form = False
#     last_failure_state = "unknown"
#     if not healing_log_df.empty and feedback_df.empty:
#         last_heal_action = healing_log_df.iloc[-1]
#         if not issue_log_df.empty:
#             issues_before_heal = issue_log_df[issue_log_df['timestamp'] < last_heal_action['timestamp']]
#             if not issues_before_heal.empty:
#                 last_failure_state = issues_before_heal.iloc[-1]['failure_state']
#                 show_feedback_form = True

#     if show_feedback_form:
#         st.info(f"The agent tried to fix a **'{last_failure_state}'** issue with the action **'{last_heal_action['strategy']}'**. This resulted in **'{last_heal_action['status']}'**.")
#         col1, col2 = st.columns(2)
#         with col1:
#             if st.button("✅ Accept Fix", use_container_width=True):
#                 feedback = {'timestamp': [pd.Timestamp.now()], 'state': [last_failure_state], 'action': [last_heal_action['strategy']], 'outcome': [last_heal_action['status']], 'feedback': ['accepted']}
#                 pd.DataFrame(feedback).to_csv("logs/user_feedback.csv", index=False, mode='a', header=not os.path.exists("logs/user_feedback.csv"))
#                 st.success("Feedback recorded!")
#                 st.rerun()
#         with col2:
#             if st.button("❌ Reject Fix", type="primary", use_container_width=True):
#                 feedback = {'timestamp': [pd.Timestamp.now()], 'state': [last_failure_state], 'action': [last_heal_action['strategy']], 'outcome': [last_heal_action['status']], 'feedback': ['rejected']}
#                 pd.DataFrame(feedback).to_csv("logs/user_feedback.csv", index=False, mode='a', header=not os.path.exists("logs/user_feedback.csv"))
#                 st.error("Rejection recorded!")
#                 st.rerun()
#     elif not feedback_df.empty:
#         st.success("Feedback has been recorded and will be applied on the next run.")
#     else:
#         st.info("No healing actions awaiting feedback.")

#     st.header("RL Optimizer Policy (Q-Table)")
#     if not q_table_df.empty:
#         st.info("This table shows the agent's learned score for each action. Higher scores (brighter colors) are better.")
#         q_table_df.index.name = "Failure State"
        
#         # --- THIS IS THE FIX ---
#         # 1. Create a copy to modify for display.
#         q_table_to_display = q_table_df.copy()
        
#         # 2. Check if the 'anomaly_score' row exists and drop it.
#         if 'anomaly_score' in q_table_to_display.index:
#             q_table_to_display = q_table_to_display.drop('anomaly_score')
        
#         # 3. Use st.dataframe with a background gradient.
#         st.dataframe(q_table_to_display.style.background_gradient(cmap='viridis').format("{:.3f}"), use_container_width=True)
#     else:
#         st.warning("`logs/rl_log.csv` not found.")

# # =======================================================
# # TAB 3: SYSTEM HEALTH SUMMARY
# # =======================================================
# with tab3:
#     st.header("🩺 System Health Metrics")

#     col1, col2, col3 = st.columns(3)

#     # --- Uptime % ---
#     uptime_percent = 100.0
#     if not uptime_df.empty and len(uptime_df) > 1:
#         uptime_df_sorted = uptime_df.sort_values('timestamp').dropna(subset=['timestamp'])
#         if not uptime_df_sorted.empty and len(uptime_df_sorted) > 1:
#             total_duration = (uptime_df_sorted['timestamp'].iloc[-1] - uptime_df_sorted['timestamp'].iloc[0]).total_seconds()
#             downtime_duration = 0
#             for i in range(len(uptime_df_sorted) - 1):
#                 if uptime_df_sorted['status'].iloc[i] == 'DOWN':
#                     downtime_duration += (uptime_df_sorted['timestamp'].iloc[i+1] - uptime_df_sorted['timestamp'].iloc[i]).total_seconds()
#             if total_duration > 0: uptime_percent = max(0, (1 - (downtime_duration / total_duration)) * 100)
    
#     total_error_events = len(issue_log_df) if not issue_log_df.empty else 0
#     total_fix_actions = len(healing_log_df) if not healing_log_df.empty else 0
    
#     with col1:
#         st.metric("Uptime Percentage", f"{uptime_percent:.2f}%")
#     with col2:
#         st.metric("Total Errors Detected", total_error_events)
#     with col3:
#         st.metric("Total Fix Actions Logged", total_fix_actions)

#     st.subheader("Error Type Breakdown")
#     if not issue_log_df.empty:
#         st.bar_chart(issue_log_df['failure_state'].value_counts())
#     else:
#         st.info("No errors recorded yet.")

#     st.subheader("Top Healing Strategies Used")
#     if not healing_log_df.empty:
#         st.bar_chart(healing_log_df['strategy'].value_counts())
#     else:
#         st.info("No healing strategies logged yet.")

# # =======================================================
# # TAB 4: RAW DATA LOGS
# # =======================================================
# with tab4:
#     st.header("📂 Raw Data Logs")
#     log_sections = {
#         "Deployment Log": deploy_log_df,
#         "Uptime Log": uptime_df,
#         "Healing Log": healing_log_df,
#         "RL Q-Table": q_table_df,
#         "User Feedback Log": feedback_df,
#         "Issue Log": issue_log_df,
#         "Patient Health": health_df
#     }
#     for name, df in log_sections.items():
#         with st.expander(f"Show {name}"):
#             if not df.empty:
#                 st.dataframe(df, use_container_width=True)
#             else:
#                 st.info(f"Log/Data for {name} is empty.")








# import streamlit as st
# import pandas as pd
# import os
# import plotly.express as px
# import datetime

# # --- Page Configuration ---
# st.set_page_config(
#     page_title="Intelligent Agent Control Board",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # --- Data Loading (Robust Version) ---
# @st.cache_data(ttl=5)
# def load_data():
#     data = {}
#     files = {
#         "deploy_log": "logs/deployment_log.csv",
#         "uptime": "logs/uptime_log.csv",
#         "healing_log": "logs/healing_log.csv",
#         "q_table": "logs/rl_log.csv",
#         "scores": "dataset/student_scores.csv",
#         "health": "dataset/patient_health.csv",
#         "feedback": "logs/user_feedback.csv",
#         "issue_log": "logs/issue_log.csv",
#         "reward_trend": "logs/rl_performance_log.csv",      # New file for RL reward trends
#         "supervisor_override": "logs/supervisor_override_log.csv"
#     }
#     for key, filename in files.items():
#         if os.path.exists(filename):
#             try:
#                 if key == "q_table":
#                     data[key] = pd.read_csv(filename, index_col=0)
#                 else:
#                     data[key] = pd.read_csv(filename)
#             except (pd.errors.ParserError, pd.errors.EmptyDataError):
#                 st.error(f"Error parsing `{filename}`. Please check the file.")
#                 data[key] = pd.DataFrame()
#         else:
#             data[key] = pd.DataFrame()
#     return data

# data_frames = load_data()
# deploy_log_df = data_frames["deploy_log"]
# uptime_df = data_frames["uptime"]
# healing_log_df = data_frames["healing_log"]
# q_table_df = data_frames["q_table"]
# scores_df = data_frames["scores"]
# health_df = data_frames["health"]
# feedback_df = data_frames["feedback"]
# issue_log_df = data_frames["issue_log"]
# reward_trend_df = data_frames.get("reward_trend", pd.DataFrame())
# supervisor_override_df = data_frames.get("supervisor_override", pd.DataFrame())

# for df in [scores_df, health_df, deploy_log_df, uptime_df, healing_log_df, feedback_df, issue_log_df, reward_trend_df, supervisor_override_df]:
#     if not df.empty and 'timestamp' in df.columns:
#         df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# # --- SIDEBAR ---
# st.sidebar.header("Dashboard Filters ⚙️")
# performance_view = st.sidebar.selectbox(
#     "Select Performance View:",
#     ["Student Scores", "Patient Health"]
# )

# st.sidebar.subheader("Manual Supervisor Override")
# manual_action = st.sidebar.selectbox("Override agent control with:", ["None", "Force Heal", "Force Restart"])
# if st.sidebar.button("Apply Override"):
#     override_log_entry = {
#         'timestamp': pd.Timestamp.now(),
#         'event_type': 'Manual Override',
#         'status': manual_action,
#         'details': 'Supervisor-initiated action'
#     }
#     override_df = pd.DataFrame([override_log_entry])
#     override_df.to_csv("logs/supervisor_override_log.csv", mode='a', header=not os.path.exists("logs/supervisor_override_log.csv"), index=False)
#     st.sidebar.success(f"Override '{manual_action}' applied and logged.")

# # --- MAIN DASHBOARD UI ---
# st.title("🤖 Intelligent Agent Control Board")
# if st.button("🔄 Refresh Data"):
#     st.rerun()

# tab1, tab2, tab3, tab4, tab5 = st.tabs([
#     "Performance & Event Timeline",
#     "Agent Intelligence",
#     "System Health Summary",
#     "RL Analytics",
#     "Raw Data Logs"
# ])

# # TAB 1: PERFORMANCE & EVENTS
# with tab1:
#     st.header(f"{performance_view} Performance")
#     if performance_view == "Student Scores":
#         if not scores_df.empty and 'timestamp' in scores_df.columns:
#             avg_scores = scores_df.groupby(scores_df['timestamp'].dt.date)['score'].mean().reset_index()
#             fig = px.line(avg_scores, x='timestamp', y='score', markers=True,
#                           labels={'timestamp': 'Date', 'score': 'Average Score'}, template="plotly_dark")
#             fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False, title=None)
#             for _, row in deploy_log_df.iterrows():
#                 if pd.notna(row['timestamp']):
#                     fig.add_vline(x=str(row['timestamp'].date()), line_width=1.5, line_dash="dash",
#                                   line_color="green" if row['status'] == 'success' else "red")
#             st.plotly_chart(fig, use_container_width=True)
#         else:
#             st.warning("`dataset/student_scores.csv` missing or invalid.")
#     elif performance_view == "Patient Health":
#         if not health_df.empty and 'timestamp' in health_df.columns:
#             df_to_plot = health_df.sort_values('timestamp').copy()
#             col1, col2 = st.columns(2)
#             with col1:
#                 st.subheader("Heart Rate")
#                 fig_hr = px.line(df_to_plot, x='timestamp', y='heart_rate', markers=True, template="plotly_dark")
#                 st.plotly_chart(fig_hr, use_container_width=True)
#             with col2:
#                 st.subheader("Oxygen Level")
#                 fig_o2 = px.line(df_to_plot, x='timestamp', y='oxygen_level', markers=True, template="plotly_dark")
#                 st.plotly_chart(fig_o2, use_container_width=True)
#         else:
#             st.warning("`dataset/patient_health.csv` missing or invalid.")

#     st.header("Combined Event Timeline")
#     logs_to_combine = []
#     if not deploy_log_df.empty: logs_to_combine.append(deploy_log_df.rename(columns={'action_type': 'event_type'}))
#     if not uptime_df.empty: logs_to_combine.append(uptime_df.rename(columns={'status': 'event_type', 'event': 'details'}))
#     if not healing_log_df.empty: logs_to_combine.append(healing_log_df.rename(columns={'strategy': 'event_type'}))
#     if not issue_log_df.empty: logs_to_combine.append(issue_log_df.rename(columns={'failure_state': 'event_type', 'reason': 'details'}))
#     if supervisor_override_df is not None and not supervisor_override_df.empty:
#         logs_to_combine.append(supervisor_override_df)
#     if logs_to_combine:
#         all_logs = pd.concat(logs_to_combine, ignore_index=True)
#         if 'timestamp' in all_logs.columns:
#             all_logs = all_logs.sort_values(by='timestamp', ascending=False)
#             display_cols = [col for col in ['timestamp', 'event_type', 'status', 'details', 'dataset_changed'] if col in all_logs.columns]
#             st.dataframe(all_logs[display_cols], use_container_width=True)
#     else:
#         st.warning("No log data available.")

# # TAB 2: AGENT INTELLIGENCE
# with tab2:
#     st.header("Healing Agent Performance")
#     if not healing_log_df.empty:
#         success_rate = (healing_log_df['status'] == 'success').sum() / len(healing_log_df) * 100
#         col1, col2 = st.columns(2)
#         with col1: st.metric("Total Healing Attempts", len(healing_log_df))
#         with col2: st.metric("Healing Success Rate", f"{success_rate:.1f}%")
#     else:
#         st.info("No healing actions logged yet.")
#     st.header("Success/Failure Ratio")
#     if not healing_log_df.empty:
#         success_count = (healing_log_df['status'] == 'success').sum()
#         fail_count = (healing_log_df['status'] == 'failure').sum()
#         ratio_fig = px.pie(
#             names=["Success", "Failure"],
#             values=[success_count, fail_count],
#             title="Healing Success/Failure Ratio"
#         )
#         st.plotly_chart(ratio_fig, use_container_width=True)
#     else:
#         st.info("No healing attempts log.")

# # TAB 3: SYSTEM HEALTH SUMMARY
# with tab3:
#     st.header("🩺 System Health Metrics")
#     col1, col2, col3 = st.columns(3)
#     uptime_percent = 100.0
#     if not uptime_df.empty and len(uptime_df) > 1:
#         uptime_df_sorted = uptime_df.sort_values('timestamp').dropna(subset=['timestamp'])
#         if not uptime_df_sorted.empty and len(uptime_df_sorted) > 1:
#             total_duration = (uptime_df_sorted['timestamp'].iloc[-1] - uptime_df_sorted['timestamp'].iloc[0]).total_seconds()
#             downtime_duration = 0
#             for i in range(len(uptime_df_sorted) - 1):
#                 if uptime_df_sorted['status'].iloc[i] == 'DOWN':
#                     downtime_duration += (uptime_df_sorted['timestamp'].iloc[i+1] - uptime_df_sorted['timestamp'].iloc[i]).total_seconds()
#             if total_duration > 0: uptime_percent = max(0, (1 - (downtime_duration / total_duration)) * 100)
#     total_error_events = len(issue_log_df) if not issue_log_df.empty else 0
#     total_fix_actions = len(healing_log_df) if not healing_log_df.empty else 0
#     with col1:
#         st.metric("Uptime Percentage", f"{uptime_percent:.2f}%")
#     with col2:
#         st.metric("Total Errors Detected", total_error_events)
#     with col3:
#         st.metric("Total Fix Actions Logged", total_fix_actions)
#     st.subheader("Error Type Breakdown")
#     if not issue_log_df.empty:
#         st.bar_chart(issue_log_df['failure_state'].value_counts())
#     else:
#         st.info("No errors recorded yet.")
#     st.subheader("Top Healing Strategies Used")
#     if not healing_log_df.empty:
#         st.bar_chart(healing_log_df['strategy'].value_counts())
#     else:
#         st.info("No healing strategies logged yet.")

#     st.subheader("System Uptime Timeline")
#     if not uptime_df.empty and 'timestamp' in uptime_df.columns:
#         uptime_df_sorted = uptime_df.sort_values('timestamp')
#         fig_uptime = px.line(uptime_df_sorted, x='timestamp', y='status', title="Real-time System Uptime")
#         st.plotly_chart(fig_uptime, use_container_width=True)

# # TAB 4: RL ANALYTICS
# with tab4:
#     st.header("Q-Table Heatmap (Actions vs States)")
#     if not q_table_df.empty:
#         st.info("Q-table: agent's learned values (actions vs. states). Brighter = higher expected reward.")
#         st.dataframe(q_table_df.style.background_gradient(cmap='viridis').format("{:.3f}"), use_container_width=True)
#         fig_q = px.imshow(q_table_df, 
#             labels=dict(x="Action", y="Failure State", color="Q-Value"),
#             color_continuous_scale='viridis')
#         st.plotly_chart(fig_q, use_container_width=True)
#     else:
#         st.warning("RL Q-table log not found.")

#     st.header("Reward Trend Over Episodes")
#     if not reward_trend_df.empty:
#         fig_r = px.line(reward_trend_df, x='episode', y='reward', title="Reward per RL Episode", markers=True)
#         st.plotly_chart(fig_r, use_container_width=True)
#     else:
#         st.info("No reward trend log available.")

# # TAB 5: RAW DATA LOGS
# with tab5:
#     st.header("📂 Raw Data Logs")
#     log_sections = {
#         "Deployment Log": deploy_log_df,
#         "Uptime Log": uptime_df,
#         "Healing Log": healing_log_df,
#         "RL Q-Table": q_table_df,
#         "User Feedback Log": feedback_df,
#         "Issue Log": issue_log_df,
#         "RL Reward Trend Log": reward_trend_df,
#         "Supervisor Override Log": supervisor_override_df
#     }
#     for name, df in log_sections.items():
#         with st.expander(f"Show {name}"):
#             if not df.empty:
#                 st.dataframe(df, use_container_width=True)
#             else:
#                 st.info(f"Log/Data for {name} is empty.")

# Note: ensure your RL agent and supervisor actions append logs to expected CSV files.







import streamlit as st
import pandas as pd
import os
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="Intelligent Agent Control Board",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Data Loading (Robust Version) ---
@st.cache_data(ttl=5)
def load_data():
    """Loads all data sources, handling file errors and parsing issues gracefully."""
    data = {}
    files = {
        "deploy_log": "logs/deployment_log.csv",
        "uptime": "logs/uptime_log.csv",
        "healing_log": "logs/healing_log.csv",
        "q_table": "logs/rl_log.csv",
        "scores": "dataset/student_scores.csv",
        "health": "dataset/patient_health.csv",
        "feedback": "logs/user_feedback.csv",
        "issue_log": "logs/issue_log.csv",
        "reward_trend": "logs/rl_performance_log.csv",
        "supervisor_override": "logs/supervisor_override_log.csv"
    }
    for key, filename in files.items():
        if os.path.exists(filename):
            try:
                if key == "q_table":
                    data[key] = pd.read_csv(filename, index_col=0)
                else:
                    data[key] = pd.read_csv(filename)
            except (pd.errors.ParserError, pd.errors.EmptyDataError):
                st.error(f"Error parsing `{filename}`. The file may be corrupted. Please delete it and re-run the simulation.")
                data[key] = pd.DataFrame()
        else:
            data[key] = pd.DataFrame()
    return data

# --- Load and Preprocess Data ---
data_frames = load_data()
deploy_log_df = data_frames["deploy_log"]
uptime_df = data_frames["uptime"]
healing_log_df = data_frames["healing_log"]
q_table_df = data_frames["q_table"]
scores_df = data_frames["scores"]
health_df = data_frames["health"]
feedback_df = data_frames["feedback"]
issue_log_df = data_frames["issue_log"]
reward_trend_df = data_frames.get("reward_trend", pd.DataFrame())
supervisor_override_df = data_frames.get("supervisor_override", pd.DataFrame())

for df in [scores_df, health_df, deploy_log_df, uptime_df, healing_log_df, feedback_df, issue_log_df, reward_trend_df, supervisor_override_df]:
    if not df.empty and 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# --- SIDEBAR ---
st.sidebar.header("Dashboard Filters ⚙️")
performance_view = st.sidebar.selectbox(
    "Select Performance View:",
    ["Student Scores", "Patient Health"]
)

st.sidebar.subheader("Manual Supervisor Override")
manual_action = st.sidebar.selectbox("Override agent control with:", ["None", "Force Heal", "Force Restart"])
if st.sidebar.button("Apply Override"):
    override_log_entry = {
        'timestamp': pd.Timestamp.now(),
        'event_type': 'Manual Override',
        'status': manual_action,
        'details': 'Supervisor-initiated action'
    }
    override_df = pd.DataFrame([override_log_entry])
    override_df.to_csv("logs/supervisor_override_log.csv", mode='a', header=not os.path.exists("logs/supervisor_override_log.csv"), index=False)
    st.sidebar.success(f"Override '{manual_action}' applied and logged.")

# --- MAIN DASHBOARD UI ---
st.title("🤖 Intelligent Agent Control Board")

# --- THIS IS THE FIX ---
# Removed the auto-refresh caption and added a manual refresh button.
if st.button("🔄 Refresh Data"):
    st.rerun()
# -------------------------

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Performance & Event Timeline",
    "Agent Intelligence",
    "System Health Summary",
    "RL Analytics",
    "Raw Data Logs"
])

# =======================================================
# TAB 1: PERFORMANCE & EVENTS
# =======================================================
with tab1:
    st.header(f"{performance_view} Performance")
    if performance_view == "Student Scores":
        if not scores_df.empty and 'timestamp' in scores_df.columns:
            avg_scores = scores_df.groupby(scores_df['timestamp'].dt.date)['score'].mean().reset_index()
            fig = px.line(avg_scores, x='timestamp', y='score', markers=True,
                          labels={'timestamp': 'Date', 'score': 'Average Score'}, template="plotly_dark")
            fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False, title=None)
            for _, row in deploy_log_df.iterrows():
                if pd.notna(row['timestamp']):
                    fig.add_vline(x=str(row['timestamp'].date()), line_width=1.5, line_dash="dash",
                                  line_color="green" if row['status'] == 'success' else "red")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("`dataset/student_scores.csv` missing or invalid.")
    elif performance_view == "Patient Health":
        if not health_df.empty and 'timestamp' in health_df.columns:
            df_to_plot = health_df.sort_values('timestamp').copy()
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Heart Rate")
                fig_hr = px.line(df_to_plot, x='timestamp', y='heart_rate', markers=True, template="plotly_dark")
                st.plotly_chart(fig_hr, use_container_width=True)
            with col2:
                st.subheader("Oxygen Level")
                fig_o2 = px.line(df_to_plot, x='timestamp', y='oxygen_level', markers=True, template="plotly_dark")
                st.plotly_chart(fig_o2, use_container_width=True)
        else:
            st.warning("`dataset/patient_health.csv` missing or invalid.")

    st.header("Combined Event Timeline")
    logs_to_combine = []
    if not deploy_log_df.empty: logs_to_combine.append(deploy_log_df.rename(columns={'action_type': 'event_type'}))
    if not uptime_df.empty: logs_to_combine.append(uptime_df.rename(columns={'status': 'event_type', 'event': 'details'}))
    if not healing_log_df.empty: logs_to_combine.append(healing_log_df.rename(columns={'strategy': 'event_type'}))
    if not issue_log_df.empty: logs_to_combine.append(issue_log_df.rename(columns={'failure_state': 'event_type', 'reason': 'details'}))
    if supervisor_override_df is not None and not supervisor_override_df.empty:
        logs_to_combine.append(supervisor_override_df)
    if logs_to_combine:
        all_logs = pd.concat(logs_to_combine, ignore_index=True)
        if 'timestamp' in all_logs.columns:
            all_logs = all_logs.sort_values(by='timestamp', ascending=False)
            display_cols = [col for col in ['timestamp', 'event_type', 'status', 'details', 'dataset_changed'] if col in all_logs.columns]
            st.dataframe(all_logs[display_cols], use_container_width=True)
    else:
        st.warning("No log data available.")

# =======================================================
# TAB 2: AGENT INTELLIGENCE
# =======================================================
with tab2:
    st.header("Healing Agent Performance")
    if not healing_log_df.empty:
        success_rate = (healing_log_df['status'] == 'success').sum() / len(healing_log_df) * 100
        col1, col2 = st.columns(2)
        with col1: st.metric("Total Healing Attempts", len(healing_log_df))
        with col2: st.metric("Healing Success Rate", f"{success_rate:.1f}%")
    else:
        st.info("No healing actions logged yet.")
    
    st.header("Success/Failure Ratio")
    if not healing_log_df.empty:
        success_count = (healing_log_df['status'] == 'success').sum()
        fail_count = (healing_log_df['status'] == 'failure').sum()
        ratio_fig = px.pie(
            names=["Success", "Failure"],
            values=[success_count, fail_count],
            title="Healing Success/Failure Ratio"
        )
        st.plotly_chart(ratio_fig, use_container_width=True)
    else:
        st.info("No healing attempts log.")

# =======================================================
# TAB 3: SYSTEM HEALTH SUMMARY
# =======================================================
with tab3:
    st.header("🩺 System Health Metrics")
    col1, col2, col3 = st.columns(3)
    uptime_percent = 100.0
    if not uptime_df.empty and len(uptime_df) > 1:
        uptime_df_sorted = uptime_df.sort_values('timestamp').dropna(subset=['timestamp'])
        if not uptime_df_sorted.empty and len(uptime_df_sorted) > 1:
            total_duration = (uptime_df_sorted['timestamp'].iloc[-1] - uptime_df_sorted['timestamp'].iloc[0]).total_seconds()
            downtime_duration = 0
            for i in range(len(uptime_df_sorted) - 1):
                if uptime_df_sorted['status'].iloc[i] == 'DOWN':
                    downtime_duration += (uptime_df_sorted['timestamp'].iloc[i+1] - uptime_df_sorted['timestamp'].iloc[i]).total_seconds()
            if total_duration > 0: uptime_percent = max(0, (1 - (downtime_duration / total_duration))* 100)
    
    total_error_events = len(issue_log_df) if not issue_log_df.empty else 0
    total_fix_actions = len(healing_log_df) if not healing_log_df.empty else 0
    
    with col1:
        st.metric("Uptime Score", f"{uptime_percent:.2f}%")
    with col2:
        st.metric("Total Errors Detected", total_error_events)
    with col3:
        st.metric("Total Fix Actions Logged", total_fix_actions)
    
    st.subheader("Error Type Breakdown")
    if not issue_log_df.empty:
        error_counts = issue_log_df['failure_state'].value_counts().reset_index()
        error_counts.columns = ['Failure State', 'Count']
        fig_err = px.bar(error_counts, x='Failure State', y='Count', color='Failure State', template="plotly_dark")
        fig_err.update_layout(xaxis_tickangle=0)
        st.plotly_chart(fig_err, use_container_width=True)
    else:
        st.info("No errors recorded yet.")
    
    st.subheader("Top Healing Strategies Used")
    if not healing_log_df.empty:
        fix_counts = healing_log_df['strategy'].value_counts().reset_index()
        fix_counts.columns = ['Strategy', 'Count']
        fig_fix = px.bar(fix_counts, x='Strategy', y='Count', color='Strategy', template="plotly_dark")
        fig_fix.update_layout(xaxis_tickangle=0)
        st.plotly_chart(fig_fix, use_container_width=True)
    else:
        st.info("No healing strategies logged yet.")

    st.subheader("System Uptime Timeline")
    if not uptime_df.empty and 'timestamp' in uptime_df.columns:
        uptime_df['status_val'] = uptime_df['status'].apply(lambda x: 1 if x == 'UP' else 0)
        fig_uptime = px.area(uptime_df, x='timestamp', y='status_val', title='System Status (1=UP, 0=DOWN)',
                             template="plotly_dark")
        fig_uptime.update_yaxes(range=[0, 1.1])
        st.plotly_chart(fig_uptime, use_container_width=True)

# =======================================================
# TAB 4: RL ANALYTICS
# =======================================================
with tab4:
    st.header("Q-Table Heatmap (Actions vs States)")
    if not q_table_df.empty:
        st.info("Q-table: agent's learned values. Brighter colors = higher expected reward.")
        
        q_table_df.index.name = "Failure State"
        st.dataframe(q_table_df.style.background_gradient(cmap='viridis').format("{:.3f}"), use_container_width=True)
    else:
        st.warning("RL Q-table log not found.")

    st.header("Reward Trend Over Episodes")
    if not reward_trend_df.empty:
        fig_r = px.line(reward_trend_df, x='timestamp', y='reward', title="Reward per RL Episode", markers=True,
                        labels={'timestamp': 'Episode (Time)', 'reward': 'Reward Received'})
        st.plotly_chart(fig_r, use_container_width=True)
    else:
        st.info("No reward trend log available.")

# =======================================================
# TAB 5: RAW DATA LOGS
# =======================================================
with tab5:
    st.header("📂 Raw Data Logs")
    log_sections = {
        "Deployment Log": deploy_log_df,
        "Uptime Log": uptime_df,
        "Healing Log": healing_log_df,
        "RL Q-Table": q_table_df,
        "User Feedback Log": feedback_df,
        "Issue Log": issue_log_df,
        "RL Reward Trend Log": reward_trend_df,
        "Supervisor Override Log": supervisor_override_df
    }
    for name, df in log_sections.items():
        with st.expander(f"Show {name}"):
            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else:
                st.info(f"Log/Data for {name} is empty.")

