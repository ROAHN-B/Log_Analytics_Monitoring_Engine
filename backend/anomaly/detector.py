import dask.dataframe as dd
import os
"""
    Detects anomalies in log data based on Z-score method.
    
    Parameters:
    - log_df: Dask DataFrame with log data containing 'timestamp' and 'level' columns.
    - z_threshold: Z-score threshold to flag anomalies.
    
    Returns:
    - Dask DataFrame with anomalies flagged.
    """
   
def detect_anomaly(log_df, z_threshold=1):
    log_df['timestamp'] = dd.to_datetime(log_df['timestamp'] )
    log_df['level'] = log_df["level"].str.strip().str.upper()

    error_logs = log_df[log_df['level'] == 'ERROR']
    error_logs.compute()

    # Create minute bucket
    error_logs["minute"] = error_logs["timestamp"].dt.floor("min")

    # Count errors per minute
    error_counts = (
        error_logs
        .groupby("minute")
        .size()
        .rename("error_count")
        .reset_index()
    ).compute()

    # Compute statistics
    mean = error_counts["error_count"].mean()
    std  = error_counts["error_count"].std()

    if std == 0:
        error_counts["z_score"] = 0
        error_counts["is_anomaly"] = True
        return error_counts

    error_counts["z_score"] = (error_counts["error_count"] - mean) / std
    error_counts["is_anomaly"] = error_counts["z_score"].abs() > z_threshold

    return error_counts[error_counts["is_anomaly"]]