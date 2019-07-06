from django.contrib.auth.decorators import login_required

from scrumate.core.task.models import Task
from scrumate.general.utils import json_data


@login_required(login_url='/login/')
def task_info(request, pk, **kwargs):
    return json_data(Task, pk)
