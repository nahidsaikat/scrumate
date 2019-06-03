from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404, reverse

from scrumate.core.choices import ProjectStatus, DeliverableStatus
from scrumate.core.filters import DailyScrumFilter
from scrumate.core.forms import DeliverableForm
from scrumate.core.models import Project, Release, Issue, Deliverable, DailyScrum

User = get_user_model()


def get_dashboard_context(request, **kwargs):
    today = datetime.today()
    pending_deliverables = Deliverable.objects.filter(sprint__start_date__lte=today, sprint__end_date__gte=today,
                            status__in=[DeliverableStatus.Pending, DeliverableStatus.InProgress]).order_by('-id')[:6]
    running_projects = Project.objects.filter(status__exact=ProjectStatus.InProgress).order_by('-id')[:6]
    recent_releases = Release.objects.all().order_by('-release_date')[:6]
    recent_issues = Issue.objects.all().order_by('-raise_date')[:6]
    data = {
        'hide': True,
        'running_projects': running_projects,
        'pending_deliverables': pending_deliverables,
        'recent_releases': recent_releases,
        'recent_issues': recent_issues,
    }
    return data

@login_required(login_url='/login/')
def index(request, **kwargs):
    context = get_dashboard_context(request, **kwargs)
    return render(request, 'index.html', context)


@login_required(login_url='/login/')
def daily_scrum_entry(request, **kwargs):
    today = datetime.today().date()
    can_assign_dev = request.user.has_perm('assign_deliverable')
    if can_assign_dev:
        queryset = Deliverable.objects.filter(sprint__start_date__lte=today, sprint__end_date__gte=today).order_by('-id')
    elif hasattr(request.user, 'employee'):
        queryset = Deliverable.objects.filter(assign_date=today,
                                              assignee=getattr(request.user, 'employee')).order_by('-id')
    else:
        queryset = None

    deliverable_filter = DailyScrumFilter(request.GET, queryset=queryset)
    deliverable_list = deliverable_filter.qs
    page = request.GET.get('page', 1)

    paginator = Paginator(deliverable_list, settings.PAGE_SIZE)
    try:
        daily_scrums = paginator.page(page)
    except PageNotAnInteger:
        daily_scrums = paginator.page(1)
    except EmptyPage:
        daily_scrums = paginator.page(paginator.num_pages)

    return render(request, 'core/daily_scrum_list.html', {
        'hide': True, 'daily_scrums': daily_scrums, 'filter': deliverable_filter, 'can_assign_dev': can_assign_dev
    })


@login_required(login_url='/login/')
@permission_required('core.assign_deliverable', raise_exception=True)
def assign_dev(request, deliverable_id, **kwargs):
    instance = get_object_or_404(Deliverable, pk=deliverable_id)
    form = DeliverableForm(request.POST or None, instance=instance)

    if request.POST:
        assignee = request.POST.get('assignee')
        instance.assignee_id = assignee
        instance.save()
        return redirect('daily_scrum')

    return render(request, 'includes/single_field.html', {
        'hide': True,
        'field': form.visible_fields()[6],
        'title': 'Assign Dev',
        'url': reverse('daily_scrum'),
        'base_template': 'index.html'
    })


@login_required(login_url='/login/')
@permission_required('core.set_actual_hour', raise_exception=True)
def set_actual_hour(request, deliverable_id, **kwargs):
    return change_actual_hour(deliverable_id, request)


@login_required(login_url='/login/')
@permission_required('core.update_actual_hour', raise_exception=True)
def update_actual_hour(request, deliverable_id, **kwargs):
    return change_actual_hour(deliverable_id, request)


def change_actual_hour(deliverable_id, request):
    instance = get_object_or_404(Deliverable, id=deliverable_id)
    form = DeliverableForm(request.POST or None, instance=instance)
    if request.POST:
        actual_hour = request.POST.get('estimated_hour')
        instance.actual_hour = actual_hour
        instance.save()
        return redirect('daily_scrum')
    return render(request, 'includes/single_field.html', {
        'hide': True,
        'field': form.visible_fields()[4],
        'title': 'Set Actual Hour',
        'url': reverse('daily_scrum'),
        'base_template': 'index.html'
    })
