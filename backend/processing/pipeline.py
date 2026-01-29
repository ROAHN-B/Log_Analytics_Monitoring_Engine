# Used for structuring and executing the data processing pipeline
import dask.dataframe as dd
from backend.ingestion.loader import load_logs
from backend.ingestion.parser import parse_log_line


def build_pipeline(file_path):
    bag = load_logs(file_path)

    parsed = bag.map(parse_log_line).filter(lambda x: x is not None)

    meta = {                    # for browser understanding (JSON data)
        "timestamp": "object",
        "level": "object",
        "service": "object",
        "message": "object",
    }
    df = parsed.to_dataframe(meta=meta)
    df["timestamp"] = dd.to_datetime(df["timestamp"])
    return df
