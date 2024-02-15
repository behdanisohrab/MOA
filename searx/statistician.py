import datetime

def log_statistics(is_success, grouping, time_range, number="0"):
    file_name="searx/statistics.log"
    with open(file_name, 'a') as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} | Success: {is_success} | Time range: {time_range} | Number of results: {number}| Grouping: {grouping}\n"
        log_file.write(log_entry)
