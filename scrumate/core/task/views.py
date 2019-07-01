from datetime import datetime
from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import DetailView

from scrumate.core.project.models import Project
from scrumate.core.task.models import Task
from scrumate.general.decorators import owner_or_lead
from scrumate.core.task.filters import TaskFilter
from scrumate.core.task.forms import TaskForm
from scrumate.general.views import HistoryList


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


class TaskHistoryList(HistoryList):
    permission_required = 'scrumate.core.task_history'

    def get_task_id(self):
        return self.kwargs.get('pk')

    def get_project_id(self):
        return self.kwargs.get('project_id')

    def get_queryset(self):
        return Task.history.filter(id=self.get_task_id())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = Project.objects.get(pk=self.get_project_id())
        task = Task.objects.get(pk=self.get_task_id())

        context['project'] = project
        context['title'] = f'History of {task.name}'
        context['back_url'] = reverse('task_list', kwargs={'project_id': self.get_project_id()})
        context['base_template'] = 'general/index_project_view.html'
        return context


class TaskDetailView(DetailView):
    queryset = Task.objects.all()
    template_name = 'includes/generic_view.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs.get('project_id')
        instance = self.get_object()
        context['form'] = TaskForm(instance=instance)
        context['edit_url'] = reverse('task_edit', kwargs={'project_id': project_id, 'pk': instance.pk})
        context['list_url'] = reverse('task_list', kwargs={'project_id': project_id})
        context['title'] = instance.name
        context['project'] = Project.objects.get(pk=project_id)
        context['base_template'] = 'general/index_project_view.html'
        return context
