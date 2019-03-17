from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from .models import Project, Release, UserStory, Sprint
from .filters import ProjectFilter, ReleaseFilter, UserStoryFilter, SprintFilter
from .forms import ProjectForm, ReleaseForm, UserStoryForm, SprintForm


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
