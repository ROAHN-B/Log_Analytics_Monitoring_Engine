import streamlit as st
from backend.processing.pipeline import build_pipeline
from backend.anomaly.detector import detect_anomaly
import plotly as px


st.title("Python Based High Throughput Log Analytics Monitoring Engine")
log_df=build_pipeline(r"realtime_logs.csv")
anomaly_df=detect_anomaly(log_df).compute()
print(anomaly_df)

st.subheader("Anomalies detected in logs")

fig=px.line(anomaly_df,x="Timestamp", y="anomaly_score", title="Anomaly Scores Over Time")
st.plotly_chart(fig)

st.subheader("Anomalous Log Entries")
st.dataframe(anomaly_df)

#Filters 
threshold=st.slider("Anomaly score threshold: ",min_value=0.0,max_value=1.0,value=0.5,step=0.01)
filtered_anomalies=anomaly_df[anomaly_df['anomaly_score']>=threshold]
print(filtered_anomalies)
st.dataframe(filtered_anomalies)