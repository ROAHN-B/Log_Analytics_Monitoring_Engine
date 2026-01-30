import streamlit as st
import plotly.express as px
import os
import sys


root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

try:
    from backend.processing.pipeline import build_pipeline
    from backend.anomaly.detector import detect_anomaly
except ImportError as e:
    st.error(f"Import Error: {e}. Ensure you are running from the root directory.")
    st.stop()


st.set_page_config(page_title="Log Analytics Engine", layout="wide")

st.title("Python Based High Throughput Log Analytics Monitoring Engine")

# Sidebar Settings
st.sidebar.header("Settings")
log_file_path = st.sidebar.text_input("Log File Path", value="realtime_logs.csv")
z_threshold = st.sidebar.slider(
    "Anomaly Z-Score Threshold", min_value=1.0, max_value=10.0, value=4.0, step=0.1
)

if st.sidebar.button("Refresh Logs"):
    st.rerun()


try:
    log_df = build_pipeline(log_file_path)

    result = detect_anomaly(
        log_df,
    )

    if hasattr(result, "compute"):
        anomaly_df = result.compute()
    else:
        anomaly_df = result

    if st.checkbox("Show raw processed log summary", value=True):
        st.dataframe(log_df.head(), use_container_width=True)

    # Visualization
    if not anomaly_df.empty:
        st.subheader("Anomalies Detected in Logs")

        fig = px.line(
            anomaly_df,
            x="timestamp",
            y="z_score",
            title="Anomaly Z-Scores Over Time",
            labels={"timestamp": "Time", "z_score": "Z-Score (Anomaly Strength)"},
            markers=True,
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Anomalous Log Entries")
        st.dataframe(
            anomaly_df.sort_values("timestamp", ascending=False),
            use_container_width=True,
        )

    else:
        st.success("No anomalies detected with the current threshold.")

except FileNotFoundError:
    st.error(f"File not found: {log_file_path}. Please check the path.")
except Exception as e:
    st.error(f"An error occurred: {e}")