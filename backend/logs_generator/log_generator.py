import time
import random
import csv
from datetime import datetime

LOG_FILE = "realtime_logs.csv"

services = ["auth", "payment", "orders", "search"]
info_msgs = ["Request OK", "User login", "Cache hit"]
error_msgs = ["DB failure", "Timeout", "Null pointer"]

# Write header once
with open(LOG_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "level", "service", "message"])

print(" Real-time log producer started...")

while True:
    level = random.choices(
        ["INFO", "WARN", "ERROR"],
        weights=[0.8, 0.1, 0.1],
    )[0]

    row = [
        datetime.now().isoformat(),
        level,
        random.choice(services),
        random.choice(error_msgs if level == "ERROR" else info_msgs)
    ]

    with open(LOG_FILE, "a", newline="") as f:
        csv.writer(f).writerow(row)

    time.sleep(0.2)  # 5 logs per second