from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from .models import Task, Deliverable


def json_data(model, pk):
    instance = get_object_or_404(model, id=pk)
    data = {}
    if instance:
        data = model_to_dict(instance)
    return JsonResponse(data)


@login_required(login_url='/login/')
def task_info(request, project_id, pk, **kwargs):
    return json_data(Task, pk)


@login_required(login_url='/login/')
def deliverable_info(request, project_id, pk, **kwargs):
    return json_data(Deliverable, pk)
