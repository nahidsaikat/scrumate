from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404, reverse

from scrumate.core.choices import ProjectStatus, DeliverableStatus
from scrumate.core.filters import ProjectFilter, ReleaseFilter, UserStoryFilter, SprintFilter, IssueFilter, TaskFilter, \
    DeliverableFilter, DailyScrumFilter, SprintStatusFilter, ProjectStatusFilter
from scrumate.core.forms import ProjectForm, ReleaseForm, UserStoryForm, SprintForm, IssueForm, TaskForm, DeliverableForm, \
    DailyScrumForm
from scrumate.core.models import Project, Release, UserStory, Sprint, Issue, Task, Deliverable, DailyScrum
from scrumate.core.pdf_render import PDFRender

User = get_user_model()


def get_dashboard_context(request, **kwargs):
    # for dev dashboard
    today = datetime.today()
    deliverable_qs = Deliverable.objects.filter(sprint__start_date__lte=today, sprint__end_date__gte=today)
    pending = deliverable_qs.filter(status=DeliverableStatus.Pending)
    in_progress = deliverable_qs.filter(status=DeliverableStatus.InProgress)
    done = deliverable_qs.filter(status=DeliverableStatus.Done)

    # for other dashboard
    projects = Project.objects.filter(~Q(status=ProjectStatus.Completed))
    pending_deliverables = Deliverable.objects.filter(status__lt=DeliverableStatus.Done)

    dev = request.user.has_perm('core.dev_dashboard')

    data = {
        'running_projects': Project.objects.filter(status__exact=ProjectStatus.InProgress).count(),
        'pending': pending,
        'in_progress': in_progress,
        'done': done,
        'dev': dev,
        'projects': projects,
        'pending_deliverables': pending_deliverables
    }
    return data

@login_required(login_url='/login/')
def index(request, **kwargs):
    context = get_dashboard_context(request, **kwargs)
    return render(request, 'index.html', {'context': context})


@login_required(login_url='/login/')
def project_list(request, **kwargs):
    project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    project_list = project_filter.qs
    page = request.GET.get('page', 1)

    paginator = Paginator(project_list, settings.PAGE_SIZE)
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)

    return render(request, 'core/projects/project_list.html', {'projects': projects, 'filter': project_filter})


@login_required(login_url='/login/')
def project_add(request, **kwargs):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list', permanent=True)
    else:
        form = ProjectForm()
    title = 'New Project'
    return render(request, 'common_add.html', {'form': form, 'title': title, 'list_url_name': 'project_list'})


@login_required(login_url='/login/')
def project_edit(request, pk, **kwargs):
    instance = get_object_or_404(Project, id=pk)
    form = ProjectForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('project_list')
    title = 'Edit Project'
    return render(request, 'common_add.html', {'form': form, 'title': title, 'list_url_name': 'project_list'})


@login_required(login_url='/login/')
@permission_required('core.update_project_status', raise_exception=True)
def update_project_status(request, pk, **kwargs):
    instance = get_object_or_404(Project, id=pk)
    form = ProjectForm(request.POST or None, instance=instance)
    if request.POST:
        status = request.POST.get('status')
        instance.status = status
        instance.save()
        return redirect('project_list')
    return render(request, 'includes/single_field.html', {
        'field': form.visible_fields()[3],
        'title': 'Update Status',
        'url': reverse('project_list')
    })


@login_required(login_url='/login/')
@permission_required('core.view_commit_logs', raise_exception=True)
def view_commit_logs(request, pk, **kwargs):
    instance = get_object_or_404(Project, id=pk)
    page = request.GET.get('page', 1)

    paginator = Paginator(instance.get_commit_messages(), settings.PAGE_SIZE)
    try:
        commit_messages = paginator.page(page)
    except PageNotAnInteger:
        commit_messages = paginator.page(1)
    except EmptyPage:
        commit_messages = paginator.page(paginator.num_pages)

    return render(request, 'core/projects/commit_logs.html', {
        'project': instance,
        'commit_messages': commit_messages
    })


@login_required(login_url='/login/')
@permission_required('core.project_status_report', raise_exception=True)
def project_status_report(request, **kwargs):
    project_status_filter = ProjectStatusFilter(request.GET, queryset=Release.objects.all())
    release_list = project_status_filter.qs
    project = Project.objects.get(pk=request.GET.get('project')) if request.GET.get('project') else None

    if not request.GET.get('project', False):
        release_list = []

    return render(request, 'core/projects/project_status.html', {
        'release_list': release_list,
        'filter': project_status_filter,
        'project': project
    })


@login_required(login_url='/login/')
@permission_required('core.project_status_report_download', raise_exception=True)
def project_status_report_download(request, pk, **kwargs):
    release_list = Release.objects.filter(project_id=pk)
    project = Project.objects.get(pk=pk)

    return PDFRender.render('core/projects/project_status_pdf.html', {
        'release_list': release_list,
        'project_name': project.name
    })


@login_required(login_url='/login/')
def release_list(request, **kwargs):
    release_filter = ReleaseFilter(request.GET, queryset=Release.objects.all())
    release_list = release_filter.qs
    page = request.GET.get('page', 1)

    paginator = Paginator(release_list, settings.PAGE_SIZE)
    try:
        releases = paginator.page(page)
    except PageNotAnInteger:
        releases = paginator.page(1)
    except EmptyPage:
        releases = paginator.page(paginator.num_pages)

    return render(request, 'core/release_list.html', {'releases': releases, 'filter': release_filter})


@login_required(login_url='/login/')
def release_add(request, **kwargs):
    if request.method == 'POST':
        form = ReleaseForm(request.POST)
        if form.is_valid():
            release = form.save(commit=False)
            release.created_by = request.user
            release.save()
            return redirect('release_list', permanent=True)
    else:
        form = ReleaseForm()
    title = 'New Release'
    return render(request, 'common_add.html', {'form': form, 'title': title, 'list_url_name': 'release_list'})


@login_required(login_url='/login/')
def release_edit(request, pk, **kwargs):
    instance = get_object_or_404(Release, id=pk)
    form = ReleaseForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('release_list')
    title = 'Edit Release'
    return render(request, 'common_add.html', {'form': form, 'title': title, 'list_url_name': 'release_list'})


@login_required(login_url='/login/')
def user_story_list(request, **kwargs):
    user_story_filter = UserStoryFilter(request.GET, queryset=UserStory.objects.all())
    user_story_list = user_story_filter.qs
    page = request.GET.get('page', 1)

    paginator = Paginator(user_story_list, settings.PAGE_SIZE)
    try:
        user_stories = paginator.page(page)
    except PageNotAnInteger:
        user_stories = paginator.page(1)
    except EmptyPage:
        user_stories = paginator.page(paginator.num_pages)

    return render(request, 'core/user_stories/user_story_list.html', {'user_stories': user_stories, 'filter': user_story_filter})


@login_required(login_url='/login/')
def user_story_add(request, **kwargs):
    if request.method == 'POST':
        form = UserStoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.analysed_by = getattr(request.user, 'employee', None)
            story.save()
            return redirect('user_story_list', permanent=True)
    else:
        form = UserStoryForm()
    title = 'New User Story'
    return render(request, 'core/user_stories/user_story_add.html',
                  {'form': form, 'title': title, 'list_url_name': 'user_story_list'})


@login_required(login_url='/login/')
def user_story_edit(request, pk, **kwargs):
    instance = get_object_or_404(UserStory, id=pk)
    form = UserStoryForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('user_story_list')
    title = 'Edit User Story'
    return render(request, 'core/user_stories/user_story_add.html',
                  {'form': form, 'title': title, 'list_url_name': 'user_story_list'})


@login_required(login_url='/login/')
@permission_required('core.update_user_story_status', raise_exception=True)
def update_user_story_status(request, pk, **kwargs):
    instance = get_object_or_404(UserStory, id=pk)
    form = UserStoryForm(request.POST or None, instance=instance)
    if request.POST:
        status = request.POST.get('status')
        instance.status = status
        instance.save()
        return redirect('user_story_list')
    return render(request, 'includes/single_field.html', {
        'field': form.visible_fields()[6],
        'title': 'Update Status',
        'url': reverse('user_story_list')
    })


@login_required(login_url='/login/')
@permission_required('core.update_sprint_status', raise_exception=True)
def update_sprint_status(request, pk, **kwargs):
    instance = get_object_or_404(Sprint, id=pk)
    form = SprintForm(request.POST or None, instance=instance)
    if request.POST:
        status = request.POST.get('status')
        instance.status = status
        instance.save()
        return redirect('sprint_list')
    return render(request, 'includes/single_field.html', {
        'field': form.visible_fields()[5],
        'title': 'Update Status',
        'url': reverse('sprint_list')
    })


@login_required(login_url='/login/')
@permission_required('core.sprint_status_report', raise_exception=True)
def sprint_status_report(request, **kwargs):
    sprint_status_filter = SprintStatusFilter(request.GET, queryset=Deliverable.objects.all())
    sprint_status_list = sprint_status_filter.qs
    sprint = Sprint.objects.get(pk=request.GET.get('sprint')) if request.GET.get('sprint') else None

    if not request.GET.get('sprint', False):
        sprint_status_list = []

    return render(request, 'core/sprint/sprint_status.html', {
        'sprint_status': sprint_status_list,
        'filter': sprint_status_filter,
        'sprint': sprint
    })


@login_required(login_url='/login/')
@permission_required('core.sprint_status_report_download', raise_exception=True)
def sprint_status_report_download(request, pk, **kwargs):
    sprint_status_list = Deliverable.objects.filter(sprint_id=pk)
    sprint = Sprint.objects.get(pk=pk)

    return PDFRender.render('core/sprint/sprint_status_pdf.html', {
        'sprint_status_list': sprint_status_list,
        'sprint_name': sprint.name
    })


@login_required(login_url='/login/')
def sprint_list(request, **kwargs):
    sprint_filter = SprintFilter(request.GET, queryset=Sprint.objects.all())
    sprint_list = sprint_filter.qs
    page = request.GET.get('page', 1)

    paginator = Paginator(sprint_list, settings.PAGE_SIZE)
    try:
        sprints = paginator.page(page)
    except PageNotAnInteger:
        sprints = paginator.page(1)
    except EmptyPage:
        sprints = paginator.page(paginator.num_pages)

    return render(request, 'core/sprint/sprint_list.html', {'sprints': sprints, 'filter': sprint_filter})


@login_required(login_url='/login/')
def sprint_add(request, **kwargs):
    if request.method == 'POST':
        form = SprintForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sprint_list', permanent=True)
    else:
        form = SprintForm()
    title = 'New Sprint'
    return render(request, 'core/sprint/sprint_add.html',
                  {'form': form, 'title': title, 'list_url_name': 'sprint_list'})


@login_required(login_url='/login/')
def sprint_edit(request, pk, **kwargs):
    instance = get_object_or_404(Sprint, id=pk)
    form = SprintForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('sprint_list')
    title = 'Edit Sprint'
    return render(request, 'core/sprint/sprint_add.html',
                  {'form': form, 'title': title, 'list_url_name': 'sprint_list'})


@login_required(login_url='/login/')
def task_list(request, **kwargs):
    task_filter = TaskFilter(request.GET, queryset=Task.objects.all())
    task_list = task_filter.qs
    page = request.GET.get('page', 1)

    paginator = Paginator(task_list, settings.PAGE_SIZE)
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)

    return render(request, 'core/task/task_list.html', {'tasks': tasks, 'filter': task_filter})


@login_required(login_url='/login/')
def task_add(request, **kwargs):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = task.user_story.project
            task.release = task.user_story.release
            task.assigned_by = getattr(request.user, 'employee', None)
            task.assign_date = datetime.today()
            task.save()
            return redirect('task_list', permanent=True)
    else:
        form = TaskForm()
    title = 'New Task'
    return render(request, 'core/task/task_add.html',
                  {'form': form, 'title': title, 'list_url_name': 'task_list'})


@login_required(login_url='/login/')
def task_edit(request, pk, **kwargs):
    instance = get_object_or_404(Task, id=pk)
    form = TaskForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('task_list')
    title = 'Edit Task'
    return render(request, 'core/task/task_add.html',
                  {'form': form, 'title': title, 'list_url_name': 'task_list'})


@login_required(login_url='/login/')
@permission_required('core.update_task_status', raise_exception=True)
def update_task_status(request, pk, **kwargs):
    instance = get_object_or_404(Task, id=pk)
    form = TaskForm(request.POST or None, instance=instance)
    if request.POST:
        status = request.POST.get('status')
        instance.status = status
        instance.save()
        return redirect('task_list')
    return render(request, 'includes/single_field.html', {
        'field': form.visible_fields()[7],
        'title': 'Update Status',
        'url': reverse('task_list')
    })


@login_required(login_url='/login/')
def deliverable_list(request, **kwargs):
    deliverable_filter = DeliverableFilter(request.GET, queryset=Deliverable.objects.all())
    deliverable_list = deliverable_filter.qs
    page = request.GET.get('page', 1)

    paginator = Paginator(deliverable_list, settings.PAGE_SIZE)
    try:
        deliverables = paginator.page(page)
    except PageNotAnInteger:
        deliverables = paginator.page(1)
    except EmptyPage:
        deliverables = paginator.page(paginator.num_pages)

    return render(request, 'core/deliverable/deliverable_list.html', {'deliverables': deliverables, 'filter': deliverable_filter})


@login_required(login_url='/login/')
def deliverable_add(request, **kwargs):
    if request.method == 'POST':
        form = DeliverableForm(request.POST)
        if form.is_valid():
            deliverable = form.save(commit=False)
            deliverable.assign_date = datetime.today()
            deliverable.save()
            return redirect('deliverable_list', permanent=True)
    else:
        form = DeliverableForm()
    title = 'New Deliverable'
    return render(request, 'core/deliverable/deliverable_add.html',
                  {'form': form, 'title': title, 'list_url_name': 'deliverable_list'})


@login_required(login_url='/login/')
def deliverable_edit(request, pk, **kwargs):
    instance = get_object_or_404(Deliverable, id=pk)
    form = DeliverableForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('deliverable_list')
    title = 'Edit Deliverable'
    return render(request, 'core/deliverable/deliverable_add.html',
                  {'form': form, 'title': title, 'list_url_name': 'deliverable_list'})


@login_required(login_url='/login/')
@permission_required('core.update_deliverable_status', raise_exception=True)
def update_deliverable_status(request, pk, **kwargs):
    instance = get_object_or_404(Deliverable, id=pk)
    form = DeliverableForm(request.POST or None, instance=instance)
    if request.POST:
        status = request.POST.get('status')
        instance.status = status
        instance.save()
        return redirect('deliverable_list')
    return render(request, 'includes/single_field.html', {
        'field': form.visible_fields()[8],
        'title': 'Update Status',
        'url': reverse('deliverable_list')
    })


@login_required(login_url='/login/')
def daily_scrum_list(request, **kwargs):
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

    return render(request, 'core/daily_scrum/daily_scrum_list.html', {'daily_scrums': daily_scrums, 'filter': daily_scrum_filter})


@login_required(login_url='/login/')
def daily_scrum_add(request, **kwargs):
    if request.method == 'POST':
        form = DailyScrumForm(request.POST)
        if form.is_valid():
            daily_scrum = form.save(commit=False)
            daily_scrum.issue = daily_scrum.deliverable.task.issue
            daily_scrum.task = daily_scrum.deliverable.task
            daily_scrum.user_story = daily_scrum.deliverable.task.user_story
            daily_scrum.release = daily_scrum.deliverable.task.release
            daily_scrum.project = daily_scrum.deliverable.task.project
            daily_scrum.save()
            return redirect('daily_scrum_list', permanent=True)
    else:
        form = DailyScrumForm()
    title = 'Daily Scrum Entry'
    return render(request, 'core/daily_scrum/daily_scrum_add.html',
                  {'form': form, 'title': title, 'list_url_name': 'daily_scrum_list'})


@login_required(login_url='/login/')
def daily_scrum_edit(request, pk, **kwargs):
    instance = get_object_or_404(DailyScrum, id=pk)
    form = DailyScrumForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('daily_scrum_list')
    title = 'Edit Daily Scrum Entry'
    return render(request, 'core/daily_scrum/daily_scrum_add.html',
                  {'form': form, 'title': title, 'list_url_name': 'daily_scrum_list'})


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
        'url': reverse('daily_scrum_list')
    })


@login_required(login_url='/login/')
def issue_list(request, **kwargs):
    issue_filter = IssueFilter(request.GET, queryset=Issue.objects.all())
    issue_list = issue_filter.qs
    page = request.GET.get('page', 1)

    paginator = Paginator(issue_list, settings.PAGE_SIZE)
    try:
        issues = paginator.page(page)
    except PageNotAnInteger:
        issues = paginator.page(1)
    except EmptyPage:
        issues = paginator.page(paginator.num_pages)

    return render(request, 'core/issue_list.html', {'issues': issues, 'filter': issue_filter})


@login_required(login_url='/login/')
def issue_add(request, **kwargs):
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('issue_list', permanent=True)
    else:
        form = IssueForm()
    title = 'New Issue'
    return render(request, 'common_add.html', {'form': form, 'title': title, 'list_url_name': 'issue_list'})


@login_required(login_url='/login/')
def issue_edit(request, pk, **kwargs):
    instance = get_object_or_404(Issue, id=pk)
    form = IssueForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('issue_list')
    title = 'Edit Issue'
    return render(request, 'common_add.html', {'form': form, 'title': title, 'list_url_name': 'issue_list'})


@login_required(login_url='/login/')
@permission_required('core.update_issue_status', raise_exception=True)
def update_issue_status(request, pk, **kwargs):
    instance = get_object_or_404(Issue, id=pk)
    form = IssueForm(request.POST or None, instance=instance)
    if request.POST:
        status = request.POST.get('status')
        instance.status = status
        instance.save()
        return redirect('issue_list')
    return render(request, 'includes/single_field.html', {
        'field': form.visible_fields()[6],
        'title': 'Update Status',
        'url': reverse('issue_list')
    })
