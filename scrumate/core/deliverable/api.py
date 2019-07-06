from django.contrib.auth.decorators import login_required

from scrumate.core.deliverable.models import Deliverable
from scrumate.general.utils import json_data


@login_required(login_url='/login/')
def deliverable_info(request, pk, **kwargs):
    return json_data(Deliverable, pk)
