import time
import dask.dataframe as dd
    
from backend.config.dask_config import start_dask
from backend.ingestion.loader import load_logs
from backend.ingestion.parser import parse_log_line
from backend.processing.pipeline import build_pipeline
from backend.config.email_config import send_mail
from backend.anomaly.detector import detect_anomaly

user_mail="rohanbelsare113@gmail.com"
def main():
    # Start Dask client
    client = start_dask()
    print(client)
    print(f"Dashboard link: {client.dashboard_link}")
    print("-" * 50)
    while True:
        start_time = time.time()
        #log_df = build_pipeline("backend/logs/sample_log.log")
        log_df = build_pipeline("realtime_logs.csv")
        total_logs = log_df.count().compute()

        end_time = time.time()
        anomalies_df = detect_anomaly(log_df)
        print(anomalies_df)

        anomalies = anomalies_df[anomalies_df["is_anomaly"] == True]

        if anomalies.shape[0] == 0:
            print("No anomalies detected.")
        else:
            print(f"{anomalies.shape[0]} Anomalies detected:")
        
        for _, row in anomalies.iterrows():
            anomaly_data={
                "timestamp": row['minute'],
                "error_count": row['error_count'],
                "z_score": row['z_score']
            }
            send_mail(
                to_mail=user_mail,
                anomaly=anomaly_data
            )
        print("Anomaly Detected")

        

        print("Total logs parsed:")
        print(total_logs)
        print("Time taken:", end_time - start_time)
        time.sleep(5)

        

if __name__ == "__main__":
    main()