import streamlit as st
import plotly.express as px
import os
import sys
import pandas as pd


root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

try:
    from backend.processing.pipeline import build_pipeline
    from backend.anomaly.detector import detect_anomaly
except ImportError as e:
    st.error(f"Import Error: {e}. Ensure you are running from the root directory.")
    st.stop()

# Page configuration
st.set_page_config(page_title="Log Analytics Engine", layout="wide")

st.title("Python Based High Throughput Log Analytics Monitoring Engine")

# Sidebar Settings
st.sidebar.header("Settings")
log_file_path = st.sidebar.text_input("Log File Path", value="realtime_logs.csv")


if st.sidebar.button("Refresh Dashboard"):
    st.rerun()


try:
    
    log_df_dask = build_pipeline(log_file_path)
    
    log_data = log_df_dask.compute() 

    
    result = detect_anomaly(log_df_dask)

    
    if hasattr(result, 'compute'):
        anomaly_df = result.compute()
    else:
        anomaly_df = result

    # --- VISUALIZATIONS ---

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Log Level Distribution")
        
        if not log_data.empty:
            level_counts = log_data['level'].value_counts().reset_index()
            level_counts.columns = ['level', 'count']
            fig_pie = px.pie(
                level_counts, 
                values='count', 
                names='level', 
                title="Distribution of Log Levels",
                color='level',
                color_discrete_map={'ERROR': 'red', 'INFO': 'blue', 'WARN': 'orange', 'DEBUG': 'green'}
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No log data available for pie chart.")

    with col2:
        st.subheader("Log Levels Over Time")
        
        if not log_data.empty:
            
            fig_time = px.line(
                log_data.sort_values("timestamp"), 
                x="timestamp", 
                y="level", 
                title="Log Level Timeline",
                color_discrete_sequence=["red"] if "ERROR" in log_data['level'].values else ["blue"]
            )
            st.plotly_chart(fig_time, use_container_width=True)

    # --- ANOMALY STATUS MESSAGE ---
    st.divider()
    total_logs = len(log_data)
    error_logs_count = len(log_data[log_data['level'] == 'ERROR'])
    error_percentage = (error_logs_count / total_logs) * 100 if total_logs > 0 else 0

# Updated Status Message Logic
    if not anomaly_df.empty or error_percentage > 90:
        st.error(f"ALERT: Critical Issues Detected!")
        if error_percentage > 90:
            st.warning(f"Extremely high error rate detected: {error_percentage:.1f}%")
    else:
        st.success("System Stable: No statistical anomalies detected.")
        
        if st.checkbox("Show raw processed log summary"):
            st.dataframe(log_data.tail(20), use_container_width=True)

except FileNotFoundError:
    st.error(f"File not found: {log_file_path}. Please check the path.")
except Exception as e:
    st.error(f"An error occurred: {e}")