from datetime import datetime
from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from scrumate.core.filters import DeliverableFilter
from scrumate.core.forms import DeliverableForm
from scrumate.core.models import Deliverable, Project


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
        return redirect('deliverable_list', project_id=project_id)

    project = Project.objects.get(pk=project_id)
    return render(request, 'includes/single_field.html', {
        'field': form.visible_fields()[8],
        'title': 'Update Status',
        'url': reverse('deliverable_list', kwargs={'project_id': project_id}),
        'project': project,
        'base_template': 'general/index_project_view.html'
    })
