import streamlit as st
import plotly.express as px
import pandas as pd
import os
import sys
from streamlit_autorefresh import st_autorefresh  # Requires: pip install streamlit-autorefresh

# PATH SETUP
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from backend.processing.pipeline import build_pipeline
from backend.anomaly.detector import detect_anomaly

# PAGE CONFIG
st.set_page_config(
    page_title="Log Analytics Engine",
    layout="wide"
)

# REFRESH EVERY 9 SECONDS
st_autorefresh(interval=9000, key="datarefresh")

st.title("Python Based High Throughput Log Analytics Monitoring Engine")

# COLOR MAPPING
color_discrete_map = {'ERROR': 'red', 'WARN': 'yellow', 'INFO': 'blue'}

# SIDEBAR
st.sidebar.header("Settings")
log_file_path = st.sidebar.text_input(
    "Log File Path",
    value="realtime_logs.csv"
)

if st.sidebar.button("Refresh Dashboard"):
    st.rerun()

# LOAD DATA
try:
    log_df_dask = build_pipeline(log_file_path)
    log_data = log_df_dask.compute()

    anomaly_result = detect_anomaly(log_df_dask)
    anomaly_df = anomaly_result.compute() if hasattr(anomaly_result, "compute") else anomaly_result

# ---------------------------------------------------
# PIE CHART
# ---------------------------------------------------
    st.subheader("Log Level Distribution")

    level_counts = log_data["level"].value_counts().reset_index()
    level_counts.columns = ["level", "count"]

    pie_chart = px.pie(
        level_counts,
        names="level",
        values="count",
        title="Distribution of Log Levels",
        color="level",
        color_discrete_map=color_discrete_map
    )

    st.plotly_chart(pie_chart, use_container_width=True)

# ---------------------------------------------------
# FILTER LEVELS
# ---------------------------------------------------
    error_df = log_data[log_data["level"] == "ERROR"]
    info_df  = log_data[log_data["level"] == "INFO"]
    warn_df  = log_data[log_data["level"] == "WARN"]

# ---------------------------------------------------
# THREE TIMELINE GRAPHS
# ---------------------------------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("ERROR Logs Over Time")
        if not error_df.empty:
            fig_error = px.histogram(error_df, x="timestamp", color_discrete_sequence=['red'])
            fig_error.update_traces(marker_line_width=1, marker_line_color="black")
            st.plotly_chart(fig_error, use_container_width=True)
        else:
            st.info("No ERROR logs")

    with col2:
        st.subheader("INFO Logs Over Time")
        if not info_df.empty:
            fig_info = px.histogram(info_df, x="timestamp", color_discrete_sequence=['blue'])
            fig_info.update_traces(marker_line_width=1, marker_line_color="black")
            st.plotly_chart(fig_info, use_container_width=True)
        else:
            st.info("No INFO logs")

    with col3:
        st.subheader("WARN Logs Over Time")
        if not warn_df.empty:
            fig_warn = px.histogram(warn_df, x="timestamp", color_discrete_sequence=['yellow'])
            fig_warn.update_traces(marker_line_width=1, marker_line_color="black")
            st.plotly_chart(fig_warn, use_container_width=True)
        else:
            st.info("No WARN logs")

# ---------------------------------------------------
# ERROR TREND PER MINUTE
# ---------------------------------------------------
    st.subheader("Error Count Per Minute")

    if not error_df.empty:
        error_df["timestamp"] = pd.to_datetime(error_df["timestamp"])

        error_trend = (
            error_df
            .set_index("timestamp")
            .resample("1min")
            .size()
            .reset_index(name="error_count")
        )

        line_chart = px.line(
            error_trend,
            x="timestamp",
            y="error_count",
            title="Error Frequency"
        )
        line_chart.update_traces(line_color='red')

        st.plotly_chart(line_chart, use_container_width=True)
    else:
        st.info("No error data available")

# ---------------------------------------------------
# STATUS PANEL
# ---------------------------------------------------
    st.divider()

    total_logs = len(log_data)
    total_errors = len(error_df)
    error_percent = (total_errors / total_logs) * 100 if total_logs else 0

    if not anomaly_df.empty or error_percent > 50:
        st.error("ALERT : System Abnormal Behavior Detected")
        st.write(f"Error Percentage : {error_percent:.2f}%")
    else:
        st.success("System Stable")

# ---------------------------------------------------
# RAW DATA VIEW
# ---------------------------------------------------
    if st.checkbox("Show last 20 logs"):
        st.dataframe(log_data.tail(20), use_container_width=True)


except FileNotFoundError:
    st.error("Log file not found")
except Exception as e:
    st.error(f"Error : {e}")