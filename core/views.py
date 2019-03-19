from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from .models import Project, Release, UserStory, Sprint, Issue, Department, Designation, Employee, Client, Task, \
    Deliverable
from .filters import ProjectFilter, ReleaseFilter, UserStoryFilter, SprintFilter, IssueFilter, DepartmentFilter, \
    DesignationFilter, EmployeeFilter, ClientFilter, TaskFilter, DeliverableFilter
from .forms import ProjectForm, ReleaseForm, UserStoryForm, SprintForm, IssueForm, DepartmentForm, DesignationForm, \
    EmployeeForm, ClientForm, TaskForm, DeliverableForm, DailyScrumForm


@login_required(login_url='/login/')
def index(request, **kwargs):
    return render(request, 'index.html')


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
            form.save()
            return redirect('release_list', permanent=True)
    else:
        form = ReleaseForm()
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
            form.save()
            return redirect('user_story_list', permanent=True)
    else:
        form = UserStoryForm()
    return render(request, 'user_stories/user_story_add.html', {'form': form})


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
            form.save()
            return redirect('task_list', permanent=True)
    else:
        form = TaskForm()
    return render(request, 'task/task_add.html', {'form': form})


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
            form.save()
            return redirect('deliverable_list', permanent=True)
    else:
        form = DeliverableForm()
    return render(request, 'deliverable/deliverable_add.html', {'form': form})


@login_required(login_url='/login/')
def daily_scrum_list(request, **kwargs):
    daily_scrum_filter = DeliverableFilter(request.GET, queryset=Deliverable.objects.all())
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
            form.save()
            return redirect('daily_scrum_list', permanent=True)
    else:
        form = DailyScrumForm()
    return render(request, 'daily_scrum/daily_scrum_add.html', {'form': form})


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
            form.save()
            return redirect('employee_list', permanent=True)
    else:
        form = EmployeeForm()
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
            form.save()
            return redirect('client_list', permanent=True)
    else:
        form = ClientForm()
    return render(request, 'client/client_add.html', {'form': form})
