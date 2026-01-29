# Used for structuring and executing the data processing pipeline
import dask.dataframe as dd
from backend.ingestion.loader import load_logs
from backend.ingestion.parser import parse_log_line


def build_pipeline(file_path):
    bag = load_logs(file_path)
    # The filter ensures we skip the CSV header line if it doesn't match the regex
    parsed = bag.map(parse_log_line).filter(lambda x: x is not None)

    meta = {
        "timestamp": "object",
        "level": "object",
        "service": "object",
        "message": "object",
    }
    df = parsed.to_dataframe(meta=meta)
    df["timestamp"] = dd.to_datetime(df["timestamp"])
    return df
