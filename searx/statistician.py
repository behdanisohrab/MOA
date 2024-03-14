import datetime
import os

def log_statistics(grouping, number=""):
    file_name = "searx/statistics.log"

    try:
        with open(file_name, 'a') as log_file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
            log_entry = f"{timestamp} | Number of results: {number} | Grouping: {grouping}\n"
            log_file.write(log_entry)
    except FileNotFoundError:
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        with open(file_name, 'w') as log_file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
            log_entry = f"{timestamp} | Log file created | Number of results: {number} | Grouping: {grouping}\n"
            log_file.write(log_entry)
