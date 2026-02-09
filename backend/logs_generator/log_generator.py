import time
import random
import csv
from datetime import datetime

LOG_FILE = "realtime_logs.csv"

services = ["auth", "payment", "orders", "search"]
info_msgs = ["Request OK", "User login", "Cache hit"]
error_msgs = ["DB failure", "Timeout", "Null pointer"]

# CRITICAL FIX: Write the header names
with open(LOG_FILE, "w", newline="") as f:
    writer = csv.writer(f)

print("Real-time log producer started with Anomaly Phases...")
START_TIME = time.time()

while True:
    elapsed = time.time() - START_TIME
    
    # Simulate a "Burst" every 60 seconds for 10 seconds
    is_burst = 60 < (elapsed % 70) < 70
    
    if is_burst:
        level = random.choices(["INFO", "WARN", "ERROR"], weights=[0.1, 0.1, 0.8])[0]
        sleep_duration = 0.05 # Fast errors!
    else:
        level = random.choices(["INFO", "WARN", "ERROR"], weights=[0.85, 0.1, 0.05])[0]
        sleep_duration = 0.2

    row = [
        datetime.now().isoformat(),
        level,
        random.choice(services),
        random.choice(error_msgs if level == "ERROR" else info_msgs)
    ]

    with open(LOG_FILE, "a", newline="") as f:
        csv.writer(f).writerow(row)

    time.sleep(sleep_duration)