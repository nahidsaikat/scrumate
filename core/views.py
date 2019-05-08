from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.conf import settings

from .models import Project, Release, UserStory, Sprint, Issue, Department, Designation, Employee, Client, Task, \
    Deliverable, DailyScrum
from .filters import ProjectFilter, ReleaseFilter, UserStoryFilter, SprintFilter, IssueFilter, DepartmentFilter, \
    DesignationFilter, EmployeeFilter, ClientFilter, TaskFilter, DeliverableFilter, DailyScrumFilter
from .forms import ProjectForm, ReleaseForm, UserStoryForm, SprintForm, IssueForm, DepartmentForm, DesignationForm, \
    EmployeeForm, ClientForm, TaskForm, DeliverableForm, DailyScrumForm
from .choices import ProjectStatus, DeliverableStatus

User = get_user_model()


def get_dashboard_context(request, **kwargs):
    today = datetime.today()
    deliverable_qs = Deliverable.objects.filter(sprint__start_date__lte=today, sprint__end_date__gte=today)
    pending = deliverable_qs.filter(status=DeliverableStatus.Pending)
    in_progress = deliverable_qs.filter(status=DeliverableStatus.InProgress)
    done = deliverable_qs.filter(status=DeliverableStatus.Done)

    data = {
        'running_projects': Project.objects.filter(status__exact=ProjectStatus.InProgress).count(),
        'pending': pending,
        'in_progress': in_progress,
        'done': done,
    }
    return data

@login_required(login_url='/login/')
def index(request, **kwargs):
    context = get_dashboard_context(request, **kwargs)
    return render(request, 'index.html', {'context': context})


@login_required(login_url='/login/')
def profile(request, **kwargs):
    employee = request.user.employee if request.user and hasattr(request.user, 'employee') else None
    return render(request, 'profile.html', {'employee': employee})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})


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

    return render(request, 'projects/project_list.html', {'projects': projects, 'filter': project_filter})


@login_required(login_url='/login/')
def project_add(request, **kwargs):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list', permanent=True)
    else:
        form = ProjectForm()
    return render(request, 'projects/project_add.html', {'form': form})


@login_required(login_url='/login/')
def project_edit(request, pk, **kwargs):
    instance = get_object_or_404(Project, id=pk)
    form = ProjectForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('project_list')
    return render(request, 'projects/project_add.html', {'form': form})


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

    return render(request, 'releases/release_list.html', {'releases': releases, 'filter': release_filter})


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
    return render(request, 'releases/release_add.html', {'form': form})


@login_required(login_url='/login/')
def release_edit(request, pk, **kwargs):
    instance = get_object_or_404(Release, id=pk)
    form = ReleaseForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('release_list')
    return render(request, 'releases/release_add.html', {'form': form})


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

    return render(request, 'user_stories/user_story_list.html', {'user_stories': user_stories, 'filter': user_story_filter})


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
    return render(request, 'user_stories/user_story_add.html', {'form': form})


@login_required(login_url='/login/')
def user_story_edit(request, pk, **kwargs):
    instance = get_object_or_404(UserStory, id=pk)
    form = UserStoryForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('user_story_list')
    return render(request, 'user_stories/user_story_add.html', {'form': form})


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

    return render(request, 'sprint/sprint_list.html', {'sprints': sprints, 'filter': sprint_filter})


@login_required(login_url='/login/')
def sprint_add(request, **kwargs):
    if request.method == 'POST':
        form = SprintForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sprint_list', permanent=True)
    else:
        form = SprintForm()
    return render(request, 'sprint/sprint_add.html', {'form': form})


@login_required(login_url='/login/')
def sprint_edit(request, pk, **kwargs):
    instance = get_object_or_404(Sprint, id=pk)
    form = SprintForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('sprint_list')
    return render(request, 'sprint/sprint_add.html', {'form': form})


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

    return render(request, 'task/task_list.html', {'tasks': tasks, 'filter': task_filter})


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
    return render(request, 'task/task_add.html', {'form': form})


@login_required(login_url='/login/')
def task_edit(request, pk, **kwargs):
    instance = get_object_or_404(Task, id=pk)
    form = TaskForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('task_list')
    return render(request, 'task/task_add.html', {'form': form})


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
        'field': form.visible_fields()[8],
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

    return render(request, 'deliverable/deliverable_list.html', {'deliverables': deliverables, 'filter': deliverable_filter})


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
    return render(request, 'deliverable/deliverable_add.html', {'form': form})


@login_required(login_url='/login/')
def deliverable_edit(request, pk, **kwargs):
    instance = get_object_or_404(Deliverable, id=pk)
    form = DeliverableForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('deliverable_list')
    return render(request, 'deliverable/deliverable_add.html', {'form': form})


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

    return render(request, 'daily_scrum/daily_scrum_list.html', {'daily_scrums': daily_scrums, 'filter': daily_scrum_filter})


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
    return render(request, 'daily_scrum/daily_scrum_add.html', {'form': form})


@login_required(login_url='/login/')
def daily_scrum_edit(request, pk, **kwargs):
    instance = get_object_or_404(DailyScrum, id=pk)
    form = DailyScrumForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('daily_scrum_list')
    return render(request, 'daily_scrum/daily_scrum_add.html', {'form': form})


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

    return render(request, 'issue/issue_list.html', {'issues': issues, 'filter': issue_filter})


@login_required(login_url='/login/')
def issue_add(request, **kwargs):
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('issue_list', permanent=True)
    else:
        form = IssueForm()
    return render(request, 'issue/issue_add.html', {'form': form})


@login_required(login_url='/login/')
def issue_edit(request, pk, **kwargs):
    instance = get_object_or_404(Issue, id=pk)
    form = IssueForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('issue_list')
    return render(request, 'issue/issue_add.html', {'form': form})


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





@login_required(login_url='/login/')
def department_list(request, **kwargs):
    department_filter = DepartmentFilter(request.GET, queryset=Department.objects.all())
    department_list = department_filter.qs
    page = request.GET.get('page', 1)

    paginator = Paginator(department_list, settings.PAGE_SIZE)
    try:
        departments = paginator.page(page)
    except PageNotAnInteger:
        departments = paginator.page(1)
    except EmptyPage:
        departments = paginator.page(paginator.num_pages)

    return render(request, 'department/department_list.html', {'departments': departments, 'filter': department_filter})


@login_required(login_url='/login/')
def department_add(request, **kwargs):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department_list', permanent=True)
    else:
        form = DepartmentForm()
    return render(request, 'department/department_add.html', {'form': form})


@login_required(login_url='/login/')
def department_edit(request, pk, **kwargs):
    instance = get_object_or_404(Department, id=pk)
    form = DepartmentForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('department_list')
    return render(request, 'department/department_add.html', {'form': form})


@login_required(login_url='/login/')
def designation_list(request, **kwargs):
    designation_filter = DesignationFilter(request.GET, queryset=Designation.objects.all())
    designation_list = designation_filter.qs
    page = request.GET.get('page', 1)

    paginator = Paginator(designation_list, settings.PAGE_SIZE)
    try:
        designations = paginator.page(page)
    except PageNotAnInteger:
        designations = paginator.page(1)
    except EmptyPage:
        designations = paginator.page(paginator.num_pages)

    return render(request, 'designation/designation_list.html', {'designations': designations, 'filter': designation_filter})


@login_required(login_url='/login/')
def designation_add(request, **kwargs):
    if request.method == 'POST':
        form = DesignationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('designation_list', permanent=True)
    else:
        form = DesignationForm()
    return render(request, 'designation/designation_add.html', {'form': form})


@login_required(login_url='/login/')
def designation_edit(request, pk, **kwargs):
    instance = get_object_or_404(Designation, id=pk)
    form = DesignationForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('designation_list')
    return render(request, 'designation/designation_add.html', {'form': form})


@login_required(login_url='/login/')
def employee_list(request, **kwargs):
    employee_filter = EmployeeFilter(request.GET, queryset=Employee.objects.all())
    employee_list = employee_filter.qs
    page = request.GET.get('page', 1)

    paginator = Paginator(employee_list, settings.PAGE_SIZE)
    try:
        employees = paginator.page(page)
    except PageNotAnInteger:
        employees = paginator.page(1)
    except EmptyPage:
        employees = paginator.page(paginator.num_pages)

    return render(request, 'employee/employee_list.html', {'employees': employees, 'filter': employee_filter})


@login_required(login_url='/login/')
def employee_add(request, **kwargs):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email']
            )
            if user:
                form.cleaned_data['user_id'] = user.id
            form.save()
            return redirect('employee_list', permanent=True)
    else:
        form = EmployeeForm()
    return render(request, 'employee/employee_add.html', {'form': form})


@login_required(login_url='/login/')
def employee_edit(request, pk, **kwargs):
    instance = get_object_or_404(Employee, id=pk)
    form = EmployeeForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('employee_list')
    return render(request, 'employee/employee_add.html', {'form': form})


@login_required(login_url='/login/')
def client_list(request, **kwargs):
    client_filter = ClientFilter(request.GET, queryset=Client.objects.all())
    client_list = client_filter.qs
    page = request.GET.get('page', 1)

    paginator = Paginator(client_list, settings.PAGE_SIZE)
    try:
        clients = paginator.page(page)
    except PageNotAnInteger:
        clients = paginator.page(1)
    except EmptyPage:
        clients = paginator.page(paginator.num_pages)

    return render(request, 'client/client_list.html', {'clients': clients, 'filter': client_filter})


@login_required(login_url='/login/')
def client_add(request, **kwargs):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email']
            )
            if user:
                form.cleaned_data['user_id'] = user.id
            form.save()
            return redirect('client_list', permanent=True)
    else:
        form = ClientForm()
    return render(request, 'client/client_add.html', {'form': form})


@login_required(login_url='/login/')
def client_edit(request, pk, **kwargs):
    instance = get_object_or_404(Client, id=pk)
    form = ClientForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('client_list')
    return render(request, 'client/client_add.html', {'form': form})
