from django.conf import settings
from django.views.generic import DetailView
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, reverse, redirect, get_object_or_404

from scrumate.core.deliverable.choices import DeliverableStatus
from scrumate.core.project.models import Project
from scrumate.core.sprint.filters import SprintFilter
from scrumate.core.sprint.forms import SprintForm
from scrumate.core.sprint.models import Sprint
from scrumate.core.deliverable.models import Deliverable
from scrumate.general.views import HistoryList


@login_required(login_url='/login/')
@permission_required('core.update_sprint_status', raise_exception=True)
def update_sprint_status(request, project_id, pk, **kwargs):
    project = Project.objects.get(pk=project_id)
    instance = get_object_or_404(Sprint, id=pk)
    form = SprintForm(request.POST or None, instance=instance)
    if request.POST:
        status = request.POST.get('status')
        instance.status = status
        instance.save()
        messages.success(request, f'Status updated for "{instance.name}" successfully!')
        return redirect('sprint_list', project_id=project_id)

    return render(request, 'includes/single_field.html', {
        'field': form.visible_fields()[5],
        'title': 'Update Status',
        'url': reverse('sprint_list', kwargs={'project_id': project_id}),
        'base_template': 'general/index_project_view.html',
        'project': project
    })


@login_required(login_url='/login/')
def sprint_list(request, project_id, **kwargs):
    project = Project.objects.get(pk=project_id)
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

    return render(request, 'core/sprint/sprint_list.html', {
        'sprints': sprints, 'filter': sprint_filter, 'project': project
    })


@login_required(login_url='/login/')
def sprint_add(request, project_id, **kwargs):
    project = Project.objects.get(pk=project_id)
    if request.method == 'POST':
        form = SprintForm(request.POST)
        if form.is_valid():
            sprint = form.save(commit=False)
            sprint.project = project
            sprint.save()
            messages.success(request, f'"{sprint.name}" added successfully!')
            return redirect('sprint_list', permanent=True, project_id=project_id)
        else:
            messages.success(request, f'Invalid data!')
    else:
        form = SprintForm()
    title = 'New Sprint'
    return render(request, 'core/sprint/sprint_add.html', {
        'form': form, 'title': title, 'list_url_name': 'sprint_list', 'project': project
    })


@login_required(login_url='/login/')
def sprint_edit(request, project_id, pk, **kwargs):
    project = Project.objects.get(pk=project_id)
    instance = get_object_or_404(Sprint, id=pk)
    form = SprintForm(request.POST or None, instance=instance)
    if form.is_valid():
        sprint = form.save()
        messages.success(request, f'"{sprint.name}" updated successfully!')
        return redirect('sprint_list')
    else:
        messages.error(request, f'Invalid data!')
    title = 'Edit Sprint'
    return render(request, 'core/sprint/sprint_add.html', {
        'form': form, 'title': title, 'list_url_name': 'sprint_list', 'project': project
    })


@login_required(login_url='/login/')
def sprint_view(request, project_id, pk, **kwargs):
    project = Project.objects.get(pk=project_id)
    sprint = Sprint.objects.get(pk=pk)
    deliverable_qs = Deliverable.objects.filter(sprint=sprint)
    pending = deliverable_qs.filter(status=DeliverableStatus.Pending)
    in_progress = deliverable_qs.filter(status=DeliverableStatus.InProgress)
    done = deliverable_qs.filter(status__in=[DeliverableStatus.Done, DeliverableStatus.Delivered])

    return render(request, 'core/sprint/sprint_view.html', {
        'pending': pending,
        'in_progress': in_progress,
        'done': done,
        'running_sprint': sprint,
        'project': project
    })


class SprintHistoryList(HistoryList):
    permission_required = 'scrumate.core.sprint_history'

    def get_sprint_id(self):
        return self.kwargs.get('pk')

    def get_project_id(self):
        return self.kwargs.get('project_id')

    def get_queryset(self):
        return Sprint.history.filter(id=self.get_sprint_id())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = Project.objects.get(pk=self.get_project_id())
        sprint = Sprint.objects.get(pk=self.get_sprint_id())

        context['project'] = project
        context['title'] = f'History of {sprint.name}'
        context['back_url'] = reverse('sprint_list', kwargs={'project_id': self.get_project_id()})
        context['base_template'] = 'general/index_project_view.html'
        return context


class SprintDetailView(DetailView):
    queryset = Sprint.objects.all()
    template_name = 'includes/generic_view.html'
    context_object_name = 'department'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs.get('project_id')
        instance = self.get_object()
        context['form'] = SprintForm(instance=instance)
        context['edit_url'] = reverse('sprint_edit', kwargs={'project_id': project_id, 'pk': instance.pk})
        context['list_url'] = reverse('sprint_list', kwargs={'project_id': project_id})
        context['title'] = instance.name
        context['project'] = Project.objects.get(pk=project_id)
        context['base_template'] = 'general/index_project_view.html'
        return context
