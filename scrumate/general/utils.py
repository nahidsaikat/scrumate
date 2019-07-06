import json
from datetime import timedelta
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict


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


def json_data(model, pk):
    instance = get_object_or_404(model, id=pk)
    data = {}
    if instance:
        data = model_to_dict(instance)
    return JsonResponse(data)
