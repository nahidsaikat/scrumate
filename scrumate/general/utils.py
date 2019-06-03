import json
from datetime import timedelta


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


def generate_day_wise_label(start_date, end_date):
    count = 1
    data = {}
    for single_date in date_range(start_date, end_date):
        data[count] = single_date.strftime('%Y-%m-%d')
        count += 1
    return json.dumps(data)
