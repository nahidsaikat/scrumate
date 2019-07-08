from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import DetailView

from scrumate.core.issue.filters import IssueFilter
from scrumate.core.issue.models import Issue
from scrumate.core.issue.forms import IssueForm
from scrumate.core.project.models import Project
from scrumate.general.views import HistoryList


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
            messages.success(request, "Issue added successfully!")
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
        messages.success(request, "Issue updated successfully!")
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
        messages.success(request, "Issue status updated successfurrl!")
        return redirect('issue_list', project_id=project_id)

    return render(request, 'includes/single_field.html', {
        'field': form.visible_fields()[5],
        'title': 'Update Status',
        'url': reverse('issue_list', kwargs={'project_id': project_id}),
        'project': Project.objects.get(pk=project_id),
        'base_template': 'general/index_project_view.html'
    })


class IssueHistoryList(HistoryList):
    permission_required = 'scrumate.core.issue_history'

    def get_issue_id(self):
        return self.kwargs.get('pk')

    def get_project_id(self):
        return self.kwargs.get('project_id')

    def get_queryset(self):
        return Issue.history.filter(id=self.get_issue_id())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = Project.objects.get(pk=self.get_project_id())
        issue = Issue.objects.get(pk=self.get_issue_id())

        context['project'] = project
        context['title'] = f'History of {issue.name}'
        context['back_url'] = reverse('issue_list', kwargs={'project_id': self.get_project_id()})
        context['base_template'] = 'general/index_project_view.html'
        return context


class IssueDetailView(DetailView):
    queryset = Issue.objects.all()
    template_name = 'includes/generic_view.html'
    context_object_name = 'issue'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs.get('project_id')
        instance = self.get_object()
        context['form'] = IssueForm(instance=instance)
        context['edit_url'] = reverse('issue_edit', kwargs={'project_id': project_id, 'pk': instance.pk})
        context['list_url'] = reverse('issue_list', kwargs={'project_id': project_id})
        context['title'] = instance.name
        context['project'] = Project.objects.get(pk=project_id)
        context['base_template'] = 'general/index_project_view.html'
        return context
