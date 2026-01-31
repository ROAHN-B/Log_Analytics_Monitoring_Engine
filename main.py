from backend.config.dask_config import start_dask
from backend.processing.pipeline import build_pipeline
from backend.anomaly.detector import detect_anomaly
from backend.config.email_config import send_mail
import time
import pandas 


ADMIN_EMAIL = "rohanbelsare113@gmail.com"


def main():
    client = start_dask()
    if client:
        print(client)
        print(f"Dashboard link: {client.dashboard_link}")
        print("\n" + "=" * 50)
    else:
        print("Running in synchronous mode (No Dask Client).")

    
    while True:
        start = time.time()
        # Build log processing pipeline
        log_df = build_pipeline(r"realtime_logs.csv")

        total_logs = log_df.count().compute()
        end = time.time()

        print("Total logs parsed: \n", total_logs)
        print("Time taken:", round(end - start, 2), "seconds")

        print("\n Running anomaly detection...")

        # Detect anomalies
        anomalies_df = detect_anomaly(log_df)

        # anomalies = anomalies_df.compute()
        anomalies = anomalies_df[anomalies_df["z_score"].notna()&(anomalies_df["z_score"]!=0)]

        if anomalies.empty:
            print("No anomalies detected")
            time.sleep(60)
            continue
        else:
            print(f"🚨 {len(anomalies)} anomaly windows detected!")

        row = anomalies.sort_values(
                "z_score", key=abs, ascending=False
            ).iloc[0]

        anomaly_data = {
                "timestamp": row["timestamp"],
                "error_count": int(row["error_count"]),
                "z_score": round(float(row["z_score"]), 2),
            }

        send_mail(to_mail=ADMIN_EMAIL, anomaly=anomaly_data)
        
        print(
                f"📧 Alert sent | Time: {row['timestamp']} | "
                f"Errors: {row['error_count']} | "
                f"Z-score: {round(row['z_score'], 2)}"
            )
        time.sleep(60)
    


if __name__ == "__main__":
    main()
