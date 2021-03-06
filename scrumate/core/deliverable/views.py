from datetime import datetime
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import DetailView

from scrumate.core.deliverable.filters import DeliverableFilter
from scrumate.core.deliverable.forms import DeliverableForm
from scrumate.core.deliverable.models import Deliverable
from scrumate.core.project.models import Project
from scrumate.general.views import HistoryList


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
            messages.success(request, "Deliverable added successfully!")
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
        messages.success(request, "Deliverable updated successfully!")
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
        messages.success(request, "Deliverable status updated successfully!")
        return redirect('deliverable_list', project_id=project_id)

    project = Project.objects.get(pk=project_id)
    return render(request, 'includes/single_field.html', {
        'field': form.visible_fields()[8],
        'title': 'Update Status',
        'url': reverse('deliverable_list', kwargs={'project_id': project_id}),
        'project': project,
        'base_template': 'general/index_project_view.html'
    })


class DeliverableHistoryList(HistoryList):
    permission_required = 'scrumate.core.deliverable_history'

    def get_deliverable_id(self):
        return self.kwargs.get('pk')

    def get_project_id(self):
        return self.kwargs.get('project_id')

    def get_queryset(self):
        return Deliverable.history.filter(id=self.get_deliverable_id())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = Project.objects.get(pk=self.get_project_id())
        deliverable = Deliverable.objects.get(pk=self.get_deliverable_id())

        context['project'] = project
        context['title'] = f'History of {deliverable.name}'
        context['back_url'] = reverse('deliverable_list', kwargs={'project_id': self.get_project_id()})
        context['base_template'] = 'general/index_project_view.html'
        return context


class DeliverableDetailView(DetailView):
    queryset = Deliverable.objects.all()
    template_name = 'includes/generic_view.html'
    context_object_name = 'deliverable'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs.get('project_id')
        instance = self.get_object()
        context['form'] = DeliverableForm(instance=instance)
        context['edit_url'] = reverse('deliverable_edit', kwargs={'project_id': project_id, 'pk': instance.pk})
        context['list_url'] = reverse('deliverable_list', kwargs={'project_id': project_id})
        context['title'] = instance.name
        context['project'] = Project.objects.get(pk=project_id)
        context['base_template'] = 'general/index_project_view.html'
        return context
