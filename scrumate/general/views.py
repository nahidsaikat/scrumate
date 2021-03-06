import json
from _datetime import datetime

from django.conf import settings as django_settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.views.generic import ListView

from scrumate.core.deliverable.choices import DeliverableStatus
from scrumate.core.deliverable.models import Deliverable
from scrumate.core.issue.models import Issue
from scrumate.core.project.choices import ProjectStatus
from scrumate.core.project.models import Project
from scrumate.core.release.models import Release
from scrumate.core.sprint.models import Sprint
from scrumate.core.task.models import Task
from scrumate.core.user_story.choices import UserStoryStatus
from scrumate.core.task.choices import TaskStatus
from scrumate.core.user_story.models import UserStory
from scrumate.people.models import Department, Designation, Employee, Client


@login_required(login_url='/login/')
def settings(request, **kwargs):
    departments_count = Department.objects.count()
    designations_count = Designation.objects.count()
    employees_count = Employee.objects.count()
    clients_count = Client.objects.count()

    employee_list = Employee.objects.all()
    page = request.GET.get('page', 1)

    paginator_emp = Paginator(employee_list, django_settings.PAGE_SIZE)
    try:
        employees = paginator_emp.page(page)
    except PageNotAnInteger:
        employees = paginator_emp.page(1)
    except EmptyPage:
        employees = paginator_emp.page(paginator_emp.num_pages)

    client_list = Client.objects.all()
    page = request.GET.get('page', 1)

    paginator_cli = Paginator(client_list, django_settings.PAGE_SIZE)
    try:
        clients = paginator_cli.page(page)
    except PageNotAnInteger:
        clients = paginator_cli.page(1)
    except EmptyPage:
        clients = paginator_cli.page(paginator_cli.num_pages)

    return render(request, 'general/index_settings.html', {
        'departments_count': departments_count,
        'designations_count': designations_count,
        'employees_count': employees_count,
        'clients_count': clients_count,
        'employee_list': employees,
        'client_list': clients
    })


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
def project(request, **kwargs):
    all_project = Project.objects.all()
    pending_project = Project.objects.filter(status=ProjectStatus.Pending)
    inprogress_project = Project.objects.filter(status=ProjectStatus.InProgress)
    complete_project = Project.objects.filter(status=ProjectStatus.Completed)

    release = Release.objects.all()
    issue = Issue.objects.filter(status__in=[DeliverableStatus.Pending, DeliverableStatus.InProgress])

    data = {
        'all_project': {
            'count': all_project.count(),
            'names': json.dumps([project.name for project in all_project]),
            'total_points': json.dumps([int(project.total_point) for project in all_project])
        },
        'pending_project': {
            'count': pending_project.count(),
            'names': json.dumps([project.name for project in pending_project]),
            'total_points': json.dumps([int(project.total_point) for project in pending_project]),
            'instances': pending_project.order_by('-id')[:10]
        },
        'inprogress_project': {
            'count': inprogress_project.count(),
            'names': json.dumps([project.name for project in inprogress_project]),
            'total_points': json.dumps([int(project.total_point) for project in inprogress_project]),
            'instances': inprogress_project.order_by('-id')[:10]
        },
        'complete_project': {
            'count': complete_project.count(),
            'names': json.dumps([project.name for project in complete_project]),
            'total_points': json.dumps([int(project.total_point) for project in complete_project]),
            'instances': complete_project.order_by('-id')[:10]
        },
        'release': {
            'count': release.count(),
            'instances': release.order_by('-id')[:10]
        },
        'issue': {
            'count': issue.count(),
            'instances': issue.order_by('-id')[:10]
        }
    }

    return render(request, 'general/index_project.html', data)

@login_required(login_url='/login/')
def project_dashboard(request, project_id, **kwargs):
    today = datetime.today().date()
    deliverable_qs = Deliverable.objects.filter(project_id=project_id,
                                                sprint__start_date__lte=today, sprint__end_date__gte=today)
    pending = deliverable_qs.filter(status=DeliverableStatus.Pending)
    in_progress = deliverable_qs.filter(status=DeliverableStatus.InProgress)
    done = deliverable_qs.filter(status=DeliverableStatus.Done)

    release = Release.objects.filter(project_id=project_id)
    user_story = UserStory.objects.filter(status__in=[UserStoryStatus.Pending, UserStoryStatus.Analysing,
                                                      UserStoryStatus.AnalysisComplete, UserStoryStatus.Developing],
                                          project_id=project_id)
    task = Task.objects.filter(status__in=[TaskStatus.Pending, TaskStatus.InProgress, TaskStatus.PartiallyDone],
                               project_id=project_id)
    issue = Issue.objects.filter(status__in=[DeliverableStatus.Pending, DeliverableStatus.InProgress],
                                 project_id=project_id)

    data = {
        'project': Project.objects.get(pk=project_id),
        'pending': pending,
        'in_progress': in_progress,
        'done': done,
        'release': {
            'count': release.count(),
            'instances': release.order_by('-id')[:10]
        },
        'user_story': {
            'count': user_story.count(),
            'instances': user_story.order_by('-id')[:10]
        },
        'task': {
            'count': task.count(),
            'instances': task.order_by('-id')[:10]
        },
        'issue': {
            'count': issue.count(),
            'instances': issue.order_by('-id')[:10]
        },
    }

    return render(request, 'general/index_project_view.html', data)


class HistoryList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'includes/history.html'
    context_object_name = 'history_list'
    paginate_by = django_settings.PAGE_SIZE

    login_url = django_settings.LOGIN_URL
