from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404, reverse

from scrumate.core.choices import ProjectStatus, DeliverableStatus
from scrumate.core.filters import DailyScrumFilter
from scrumate.core.forms import DailyScrumForm
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
    daily_scrum_filter = DailyScrumFilter(request.GET, queryset=DailyScrum.objects.all())
    daily_scrum_list = daily_scrum_filter.qs
    page = request.GET.get('page', 1)

    paginator = Paginator(daily_scrum_list, settings.PAGE_SIZE)
    try:
        daily_scrums = paginator.page(page)
    except PageNotAnInteger:
        daily_scrums = paginator.page(1)
    except EmptyPage:
        daily_scrums = paginator.page(paginator.num_pages)

    return render(request, 'core/daily_scrum/daily_scrum_list.html', {
        'daily_scrums': daily_scrums, 'filter': daily_scrum_filter, 'hide': True})


@login_required(login_url='/login/')
@permission_required('core.set_actual_hour', raise_exception=True)
def set_actual_hour(request, pk, **kwargs):
    return change_actual_hour(pk, request)


@login_required(login_url='/login/')
@permission_required('core.update_actual_hour', raise_exception=True)
def update_actual_hour(request, pk, **kwargs):
    return change_actual_hour(pk, request)


def change_actual_hour(pk, request):
    instance = get_object_or_404(DailyScrum, id=pk)
    form = DailyScrumForm(request.POST or None, instance=instance)
    if request.POST:
        actual_hour = request.POST.get('actual_hour')
        instance.actual_hour = actual_hour
        instance.save()
        return redirect('daily_scrum_list')
    return render(request, 'includes/single_field.html', {
        'field': form.visible_fields()[8],
        'title': 'Set Actual Hour',
        'url': reverse('daily_scrum_list'),
        'base_template': 'general/index_sprint.html'
    })
