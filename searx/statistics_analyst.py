import re
from collections import defaultdict
from datetime import datetime

def analyze_log(file_path="statistics.log"):
    with open(file_path, 'r') as file:
        logs = file.readlines()

    counts_by_day = defaultdict(int)
    counts_by_month = defaultdict(int)
    category_searches = {'general': 0, 'images': 0, 'videos': 0}
    result_sum = 0

    for log in logs:
        date_part, _, _ = log.split('|')
        date = datetime.strptime(date_part.strip(), '%Y-%m-%d')

        counts_by_day[date.strftime('%Y-%m-%d')] += 1

        counts_by_month[date.strftime('%Y-%m')] += 1

        category_match = re.search(r'Grouping: \[\'(.*?)\'\]', log)
        if category_match:
            category = category_match.group(1)
            if category in category_searches:
                category_searches[category] += 1

        matches = re.findall(r'Number of results: ([\d,]+)', log)
        for match in matches:
            number = int(match.replace(',', ''))
            result_sum += number

    return {
        'Total': result_sum,
        'Number by day': dict(counts_by_day),
        'Number by month': dict(counts_by_month),
        'Number by category': category_searches

    }

