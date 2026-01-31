"""What is problem we need slove?
- > Services, or, Application or servers may generate a large no of log data every day
- > If sometimes errors increase suddenly, this sudden increase are called anamoly
- > Detect anamoly and send alert using webhooks(URL)

What Is Z_Score?
Z_score tells us how far a value is value is from normal behaviour

Formaula

z = x - u / sigma

What is data present in log data

1. timestamp
2. Level
3. Service
4. Message


Logs data -----> Takes only errors from log data -----> Count the errors per minute(based on log data)------->Find normal behaviour (mean) ----------> cal z scrore--------> flag anamoly ---->alert customer/organization


Import dask.dataframe as dd

Step 1: define function for anamoly delect
step 2: Count errors per minute based log data
step 3: Find the Normal behaviour
step 5: calculate z score
step 6 : Delect anamoly
step 7 : return anamoly

UPDATE:: currently using rolling z_score which
will check error consistency in every 5 minutes.
"""

import dask.dataframe as dd
import os



def detect_anomaly(log_df, z_threshold=3):
    scheduler_type = 'synchronous' if os.environ.get('RENDER') else None
    error_logs = log_df[log_df["level"] == "ERROR"]
    error_pd = error_logs.compute().sort_values("timestamp").set_index("timestamp")
    error_counts = error_pd.resample("1min").size().rename("error_count").reset_index()

    window = 5  # 5-minute rolling window so that 

   
    error_counts["rolling_mean"] = (
        error_counts["error_count"].rolling(window).mean()
    )

    error_counts["rolling_std"] = (
        error_counts["error_count"].rolling(window).std(ddof=1)
    )

  
    error_counts = error_counts[error_counts["rolling_std"] > 0]

   
    error_counts["z_score"] = (
        (error_counts["error_count"] - error_counts["rolling_mean"])
        / error_counts["rolling_std"]
    )

    
    error_counts["is_anomaly"] = (
        error_counts["z_score"].abs() > z_threshold
    )

    return error_counts[error_counts["is_anomaly"]]

