from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from scrumate.core.filters import IssueFilter
from scrumate.core.models import Issue, Project
from scrumate.core.issue.forms import IssueForm


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
