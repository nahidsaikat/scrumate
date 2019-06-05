from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from scrumate.core.project.filters import ProjectFilter
from scrumate.core.project.forms import ProjectForm
from scrumate.core.project.models import Project, ProjectCommitLog
from scrumate.general.decorators import admin_user


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


@admin_user
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
    return render(request, 'core/projects/project_add.html', {'form': form, 'title': title, 'list_url_name': 'project_list'})


@admin_user
@login_required(login_url='/login/')
def project_edit(request, project_id, **kwargs):
    instance = get_object_or_404(Project, id=project_id)
    form = ProjectForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('project_list')
    title = 'Edit Project'
    return render(request, 'core/projects/project_add.html', {'form': form, 'title': title, 'list_url_name': 'project_list'})


@login_required(login_url='/login/')
@permission_required('core.update_project_status', raise_exception=True)
def update_project_status(request, project_id, **kwargs):
    instance = get_object_or_404(Project, id=project_id)
    form = ProjectForm(request.POST or None, instance=instance)
    if request.POST:
        status = request.POST.get('status')
        instance.status = status
        instance.save()
        return redirect('project_list')
    return render(request, 'includes/single_field.html', {
        'field': form.visible_fields()[3],
        'title': 'Update Status',
        'url': reverse('project_list', kwargs={'project_id': project_id}),
        'project': instance,
        'base_template': 'general/index_project_view.html'
    })


@login_required(login_url='/login/')
@permission_required('core.view_commit_logs', raise_exception=True)
def view_commit_logs(request, project_id, **kwargs):
    project = get_object_or_404(Project, id=project_id)
    commit_log = project.commit_log
    page = request.GET.get('page', 1)

    paginator = Paginator(commit_log.order_by('-date').all(), settings.PAGE_SIZE)
    try:
        commit_log = paginator.page(page)
    except PageNotAnInteger:
        commit_log = paginator.page(1)
    except EmptyPage:
        commit_log = paginator.page(paginator.num_pages)

    return render(request, 'core/projects/commit_logs.html', {
        'project': project,
        'commit_log': commit_log
    })


@login_required(login_url='/login/')
@permission_required('core.view_commit_logs', raise_exception=True)
def sync_commit(request, project_id, **kwargs):
    project = get_object_or_404(Project, id=project_id)
    commit_list = project.commit_messages_since(since=project.last_sync_time).reversed
    last_date = None

    for commit in commit_list:
        _commit = commit.commit
        author = _commit.author
        log = ProjectCommitLog(
            project=project,
            sha=_commit.sha,
            message=_commit.message,
            date=author.date,
            author_name=author.name,
            author_email=author.email,
            url=_commit.url,
            html_url=_commit.html_url
        )
        try:
            log.save()
        except IntegrityError as e:
            print(e)
        last_date = author.date

    if last_date:
        project.last_sync_time = last_date
        project.save()

    return HttpResponseRedirect(reverse('view_commit_logs', kwargs={'project_id': project.id}))
