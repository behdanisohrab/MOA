import datetime

def log_statistics(grouping, number=""):
    file_name="searx/statistics.log"
    with open(file_name, 'a') as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        log_entry = f"{timestamp} | Number of results: {number}| Grouping: {grouping}\n"
        log_file.write(log_entry)
