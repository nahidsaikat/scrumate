from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404

from scrumate.general.decorators import project_owner
from scrumate.core.models import Project, Release
from scrumate.core.filters import ReleaseFilter
from scrumate.core.forms import ReleaseForm


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
