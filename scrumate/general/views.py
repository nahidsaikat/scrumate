from _datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from scrumate.core.choices import DeliverableStatus, ProjectStatus
from scrumate.core.models import Deliverable, Project, Sprint


@login_required(login_url='/login/')
def settings(request, **kwargs):
    employee = request.user.employee if request.user and hasattr(request.user, 'employee') else None
    return render(request, 'general/index_settings.html', {'employee': employee})


@login_required(login_url='/login/')
def reports(request, **kwargs):
    all_project_count = Project.objects.count()
    pending_project_count = Project.objects.filter(status=ProjectStatus.Pending).count()
    inprogress_project_count = Project.objects.filter(status=ProjectStatus.InProgress).count()
    complete_project_count = Project.objects.filter(status=ProjectStatus.Completed).count()

    last_5_ip_projects = Project.objects.filter(status=ProjectStatus.InProgress).order_by('-id')[:5]
    last_5_sprint = Sprint.objects.order_by('-id')[:5]

    return render(request, 'general/index_reports.html', {
        'all_project': all_project_count,
        'pending_project': pending_project_count,
        'inprogress_project': inprogress_project_count,
        'complete_project': complete_project_count,
        'last_5_ip_projects': last_5_ip_projects,
        'last_5_sprint': last_5_sprint
    })


@login_required(login_url='/login/')
def sprint(request, **kwargs):
    today = datetime.today()
    deliverable_qs = Deliverable.objects.filter(sprint__start_date__lte=today, sprint__end_date__gte=today)
    pending = deliverable_qs.filter(status=DeliverableStatus.Pending)
    in_progress = deliverable_qs.filter(status=DeliverableStatus.InProgress)
    done = deliverable_qs.filter(status=DeliverableStatus.Done)

    data = {
        'pending': pending,
        'in_progress': in_progress,
        'done': done,
    }

    return render(request, 'general/index_sprint.html', {'data': data})


@login_required(login_url='/login/')
def project(request, **kwargs):
    employee = request.user.employee if request.user and hasattr(request.user, 'employee') else None
    return render(request, 'general/index_project.html', {'employee': employee})

