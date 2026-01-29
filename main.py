from backend.confg.dask_config import start_dask
from backend.processing.pipeline import build_pipeline
from backend.anomaly.detector import detect_anomaly
from backend.config.email_config import send_anomaly_email
import time


ADMIN_EMAIL = "rohanbelsare113@gmail.com" 


def main():
    client = start_dask()
    print(client)
    print(f"Dashboard link: {client.dashboard_link}")
    print("\n" + "=" * 50)

    start = time.time()

    # Build log processing pipeline
    log_df = build_pipeline("log_generater/realtime_logs.csv")

    total_logs = log_df.count().compute()
    end = time.time()

    print("Total logs parsed:", total_logs)
    print("Time taken:", round(end - start, 2), "seconds")

    print("\n Running anomaly detection...")

    # Detect anomalies
    anomalies_df = detect_anomaly(log_df)

    # anomalies = anomalies_df.compute()
    anomalies = anomalies_df

    if anomalies.empty:
        print("No anomalies detected")
    else:
        print(f"🚨 {len(anomalies)} anomalies detected!")

        for _, row in anomalies.iterrows():
            anomaly_data = {
                "timestamp": row["timestamp"],
                "error_count": row["error_count"],
                "z_score": row["z_score"]
            }

            send_anomaly_email(
                to_email=ADMIN_EMAIL,
                anomaly=anomaly_data
            )

            print(
                f"📧 Alert sent | Time: {row['timestamp']} | "
                f"Errors: {row['error_count']}"
            )

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()