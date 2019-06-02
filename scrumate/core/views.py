from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404, reverse

from scrumate.core.choices import ProjectStatus, DeliverableStatus
from scrumate.core.filters import ReleaseFilter, UserStoryFilter, IssueFilter, TaskFilter, \
    DeliverableFilter, DailyScrumFilter
from scrumate.core.forms import ReleaseForm, UserStoryForm, IssueForm, TaskForm, DeliverableForm, \
    DailyScrumForm, ProjectMemberForm
from scrumate.core.models import Project, Release, UserStory, Issue, Task, Deliverable, DailyScrum, \
    ProjectMember
from scrumate.general.decorators import project_owner, owner_or_lead

User = get_user_model()


def get_dashboard_context(request, **kwargs):
    today = datetime.today()
    pending_deliverables = Deliverable.objects.filter(sprint__start_date__lte=today, sprint__end_date__gte=today,
                            status__in=[DeliverableStatus.Pending, DeliverableStatus.InProgress]).order_by('-id')[:6]
    running_projects = Project.objects.filter(status__exact=ProjectStatus.InProgress).order_by('-id')[:6]
    recent_releases = Release.objects.all().order_by('-release_date')[:6]
    recent_issues = Issue.objects.all().order_by('-raise_date')[:6]
    data = {
        'home': True,
        'running_projects': running_projects,
        'pending_deliverables': pending_deliverables,
        'recent_releases': recent_releases,
        'recent_issues': recent_issues,
    }
    return data

@login_required(login_url='/login/')
def index(request, **kwargs):
    context = get_dashboard_context(request, **kwargs)
    return render(request, 'index.html', {'context': context})


@login_required(login_url='/login/')
@permission_required('core.project_members', raise_exception=True)
def project_member_list(request, project_id, **kwargs):
    project = Project.objects.get(pk=project_id)

    member_list = project.projectmember_set.all()

    return render(request, 'core/projects/project_member_list.html', {
        'member_list': member_list,
        'project': project
    })


@project_owner
@login_required(login_url='/login/')
@permission_required('core.project_members', raise_exception=True)
def project_member_add(request, project_id, **kwargs):
    project = Project.objects.get(pk=project_id)
    if request.method == 'POST':
        form = ProjectMemberForm(request.POST)
        user_id = request.POST.get('user')
        already_assigned = ProjectMember.objects.filter(project_id=project_id, user_id=user_id).count()
        if already_assigned:
            form.add_error('user', 'User is already in the team!')
        elif form.is_valid():
            member = form.save(commit=False)
            member.project = project
            member.save()
            return redirect('project_member_list', permanent=True, project_id=project_id)
    else:
        form = ProjectMemberForm()

    title = 'Add Member'
    return render(request, 'core/common_add.html', {'form': form, 'title': title,
                                                    'list_url_name': 'project_member_list', 'project': project})


@project_owner
@login_required(login_url='/login/')
@permission_required('core.project_members', raise_exception=True)
def project_member_edit(request, project_id, pk, **kwargs):
    instance = get_object_or_404(ProjectMember, id=pk)
    form = ProjectMemberForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('project_member_list', permanent=True, project_id=project_id)

    title = 'Edit Member'
    project = Project.objects.get(pk=project_id)
    return render(request, 'core/common_add.html', {'form': form, 'title': title,
                                                    'list_url_name': 'project_member_list', 'project': project})


@project_owner
@login_required(login_url='/login/')
@permission_required('core.project_members', raise_exception=True)
def project_member_delete(request, project_id, pk, **kwargs):
    instance = get_object_or_404(ProjectMember, id=pk)
    if instance:
        instance.delete()
        return redirect('project_member_list', permanent=True, project_id=project_id)

    title = 'Delete Member'
    project = Project.objects.get(pk=project_id)
    return render(request, 'core/common_add.html', {'title': title,
                                                    'list_url_name': 'project_member_list', 'project': project})


@login_required(login_url='/login/')
def release_list(request, project_id, **kwargs):
    release_filter = ReleaseFilter(request.GET, queryset=Release.objects.filter(project_id=project_id).order_by('-id'))
    release_list = release_filter.qs
    page = request.GET.get('page', 1)

    paginator = Paginator(release_list, settings.PAGE_SIZE)
    try:
        releases = paginator.page(page)
    except PageNotAnInteger:
        releases = paginator.page(1)
    except EmptyPage:
        releases = paginator.page(paginator.num_pages)

    project = Project.objects.get(pk=project_id)
    return render(request, 'core/release_list.html', {'releases': releases, 'filter': release_filter, 'project': project})


@project_owner
@login_required(login_url='/login/')
def release_add(request, project_id, **kwargs):
    if request.method == 'POST':
        form = ReleaseForm(request.POST)
        if form.is_valid():
            release = form.save(commit=False)
            release.created_by = request.user
            release.project_id = project_id
            release.save()
            return redirect('release_list', permanent=True, project_id=project_id)
    else:
        form = ReleaseForm()
    title = 'New Release'
    project = Project.objects.get(pk=project_id)
    return render(request, 'core/common_add.html', {'form': form, 'title': title, 'list_url_name': 'release_list', 'project': project})


@project_owner
@login_required(login_url='/login/')
def release_edit(request, project_id, pk, **kwargs):
    instance = get_object_or_404(Release, id=pk)
    form = ReleaseForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('release_list', permanent=True, project_id=project_id)
    title = 'Edit Release'
    project = Project.objects.get(pk=project_id)
    return render(request, 'core/common_add.html', {'form': form, 'title': title, 'list_url_name': 'release_list', 'project': project})


@login_required(login_url='/login/')
def user_story_list(request, project_id, **kwargs):
    user_story_filter = UserStoryFilter(request.GET, queryset=UserStory.objects.filter(project_id=project_id).order_by('-id'))
    user_story_list = user_story_filter.qs
    page = request.GET.get('page', 1)

    paginator = Paginator(user_story_list, settings.PAGE_SIZE)
    try:
        user_stories = paginator.page(page)
    except PageNotAnInteger:
        user_stories = paginator.page(1)
    except EmptyPage:
        user_stories = paginator.page(paginator.num_pages)

    project = Project.objects.get(pk=project_id)
    return render(request, 'core/user_story_list.html', {'user_stories': user_stories, 'filter': user_story_filter, 'project': project})


@owner_or_lead
@login_required(login_url='/login/')
def user_story_add(request, project_id, **kwargs):
    if request.method == 'POST':
        form = UserStoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.analysed_by = getattr(request.user, 'employee', None)
            story.project_id = project_id
            story.save()
            return redirect('user_story_list', permanent=True, project_id=project_id)
    else:
        form = UserStoryForm()

    title = 'New User Story'
    project = Project.objects.get(pk=project_id)
    return render(request, 'core/common_add.html', {'form': form, 'title': title, 'list_url_name': 'user_story_list', 'project': project})

@owner_or_lead
@login_required(login_url='/login/')
def user_story_edit(request, project_id, pk, **kwargs):
    instance = get_object_or_404(UserStory, id=pk)
    form = UserStoryForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('user_story_list', project_id=project_id)

    title = 'Edit User Story'
    project = Project.objects.get(pk=project_id)
    return render(request, 'core/common_add.html', {'form': form, 'title': title, 'list_url_name': 'user_story_list', 'project': project})


@owner_or_lead
@login_required(login_url='/login/')
@permission_required('core.update_user_story_status', raise_exception=True)
def update_user_story_status(request, project_id, pk, **kwargs):
    instance = get_object_or_404(UserStory, id=pk)
    form = UserStoryForm(request.POST or None, instance=instance)
    if request.POST:
        status = request.POST.get('status')
        instance.status = status
        instance.save()
        return redirect('user_story_list', project_id=project_id)

    project = Project.objects.get(pk=project_id)
    return render(request, 'includes/single_field.html', {
        'field': form.visible_fields()[5],
        'title': 'Update Status',
        'url': reverse('user_story_list', kwargs={'project_id': project_id}),
        'project': project,
        'base_template': 'general/index_project_view.html'
    })


@login_required(login_url='/login/')
def task_list(request, project_id, **kwargs):
    task_filter = TaskFilter(request.GET, queryset=Task.objects.filter(project_id=project_id).order_by('-id'))
    task_list = task_filter.qs
    page = request.GET.get('page', 1)

    paginator = Paginator(task_list, settings.PAGE_SIZE)
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)

    project = Project.objects.get(pk=project_id)
    return render(request, 'core/task_list.html', {'tasks': tasks, 'filter': task_filter, 'project': project})


@owner_or_lead
@login_required(login_url='/login/')
def task_add(request, project_id, **kwargs):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = task.user_story.project
            task.release = task.user_story.release
            task.assigned_by = getattr(request.user, 'employee', None)
            task.assign_date = datetime.today()
            task.save()
            return redirect('task_list', permanent=True, project_id=project_id)
    else:
        form = TaskForm()

    title = 'New Task'
    project = Project.objects.get(pk=project_id)
    return render(request, 'core/common_add.html', {'form': form, 'title': title, 'list_url_name': 'task_list', 'project': project})


@owner_or_lead
@login_required(login_url='/login/')
def task_edit(request, project_id, pk, **kwargs):
    instance = get_object_or_404(Task, id=pk)
    form = TaskForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('task_list', project_id=project_id)

    title = 'Edit Task'
    project = Project.objects.get(pk=project_id)
    return render(request, 'core/common_add.html', {'form': form, 'title': title, 'list_url_name': 'task_list', 'project': project})


@owner_or_lead
@login_required(login_url='/login/')
@permission_required('core.update_task_status', raise_exception=True)
def update_task_status(request, project_id, pk, **kwargs):
    instance = get_object_or_404(Task, id=pk)
    form = TaskForm(request.POST or None, instance=instance)
    if request.POST:
        status = request.POST.get('status')
        instance.status = status
        instance.save()
        return redirect('task_list', project_id=project_id)

    project = Project.objects.get(pk=project_id)
    return render(request, 'includes/single_field.html', {
        'field': form.visible_fields()[7],
        'title': 'Update Status',
        'url': reverse('task_list', kwargs={'project_id': project_id}),
        'project': project,
        'base_template': 'general/index_project_view.html'
    })


@login_required(login_url='/login/')
def deliverable_list(request, project_id, **kwargs):
    deliverable_filter = DeliverableFilter(request.GET, queryset=Deliverable.objects.filter(project_id=project_id).order_by('-id'))
    deliverable_list = deliverable_filter.qs
    page = request.GET.get('page', 1)

    paginator = Paginator(deliverable_list, settings.PAGE_SIZE)
    try:
        deliverables = paginator.page(page)
    except PageNotAnInteger:
        deliverables = paginator.page(1)
    except EmptyPage:
        deliverables = paginator.page(paginator.num_pages)

    project = Project.objects.get(pk=project_id)
    return render(request, 'core/deliverable/deliverable_list.html', {'deliverables': deliverables, 'filter': deliverable_filter, 'project': project})


@login_required(login_url='/login/')
def deliverable_add(request, project_id, **kwargs):
    if request.method == 'POST':
        form = DeliverableForm(request.POST)
        if form.is_valid():
            deliverable = form.save(commit=False)
            deliverable.assign_date = datetime.today()
            deliverable.project_id = project_id
            deliverable.save()
            return redirect('deliverable_list', permanent=True, project_id=project_id)
    else:
        form = DeliverableForm()

    title = 'New Deliverable'
    project = Project.objects.get(pk=project_id)
    return render(request, 'core/deliverable/deliverable_add.html',
                  {'form': form, 'title': title, 'list_url_name': 'deliverable_list', 'project': project})


@login_required(login_url='/login/')
def deliverable_edit(request, project_id, pk, **kwargs):
    instance = get_object_or_404(Deliverable, id=pk)
    form = DeliverableForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('deliverable_list', project_id=project_id)

    title = 'Edit Deliverable'
    project = Project.objects.get(pk=project_id)
    return render(request, 'core/deliverable/deliverable_add.html',
                  {'form': form, 'title': title, 'list_url_name': 'deliverable_list', 'project': project})


@login_required(login_url='/login/')
@permission_required('core.update_deliverable_status', raise_exception=True)
def update_deliverable_status(request, project_id, pk, **kwargs):
    instance = get_object_or_404(Deliverable, id=pk)
    form = DeliverableForm(request.POST or None, instance=instance)
    if request.POST:
        status = request.POST.get('status')
        instance.status = status
        instance.save()
        return redirect('deliverable_list', project_id=project_id)

    project = Project.objects.get(pk=project_id)
    return render(request, 'includes/single_field.html', {
        'field': form.visible_fields()[8],
        'title': 'Update Status',
        'url': reverse('deliverable_list', kwargs={'project_id': project_id}),
        'project': project,
        'base_template': 'general/index_project_view.html'
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
        'url': reverse('daily_scrum_list'),
        'base_template': 'general/index_sprint.html'
    })


@login_required(login_url='/login/')
def issue_list(request, project_id, **kwargs):
    issue_filter = IssueFilter(request.GET, queryset=Issue.objects.filter(project_id=project_id).order_by('-id'))
    issue_list = issue_filter.qs
    page = request.GET.get('page', 1)

    paginator = Paginator(issue_list, settings.PAGE_SIZE)
    try:
        issues = paginator.page(page)
    except PageNotAnInteger:
        issues = paginator.page(1)
    except EmptyPage:
        issues = paginator.page(paginator.num_pages)

    project = Project.objects.get(pk=project_id)
    return render(request, 'core/issue_list.html', {'issues': issues, 'filter': issue_filter, 'project': project})


@login_required(login_url='/login/')
def issue_add(request, project_id, **kwargs):
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.project_id = project_id
            issue.save()
            return redirect('issue_list', permanent=True, project_id=project_id)
    else:
        form = IssueForm()

    title = 'New Issue'
    project = Project.objects.get(pk=project_id)
    return render(request, 'core/common_add.html', {'form': form, 'title': title, 'list_url_name': 'issue_list', 'project': project})


@login_required(login_url='/login/')
def issue_edit(request, project_id, pk, **kwargs):
    instance = get_object_or_404(Issue, id=pk)
    form = IssueForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('issue_list', project_id=project_id)

    title = 'Edit Issue'
    project = Project.objects.get(pk=project_id)
    return render(request, 'core/common_add.html', {'form': form, 'title': title, 'list_url_name': 'issue_list', 'project': project})


@login_required(login_url='/login/')
@permission_required('core.update_issue_status', raise_exception=True)
def update_issue_status(request, project_id, pk, **kwargs):
    instance = get_object_or_404(Issue, id=pk)
    form = IssueForm(request.POST or None, instance=instance)
    if request.POST:
        status = request.POST.get('status')
        instance.status = status
        instance.save()
        return redirect('issue_list', project_id=project_id)

    return render(request, 'includes/single_field.html', {
        'field': form.visible_fields()[5],
        'title': 'Update Status',
        'url': reverse('issue_list', kwargs={'project_id': project_id}),
        'project': Project.objects.get(pk=project_id),
        'base_template': 'general/index_project_view.html'
    })
