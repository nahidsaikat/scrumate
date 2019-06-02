from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from scrumate.core.models import Project, Sprint, Deliverable
from scrumate.core.forms import SprintForm
from scrumate.core.filters import SprintStatusFilter, SprintFilter
from scrumate.core.choices import DeliverableStatus
from scrumate.general.pdf_render import PDFRender


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
        return redirect('sprint_list', project_id=project_id)

    return render(request, 'includes/single_field.html', {
        'field': form.visible_fields()[5],
        'title': 'Update Status',
        'url': reverse('sprint_list', kwargs={'project_id': project_id}),
        'base_template': 'general/index_project_view.html',
        'project': project
    })


@login_required(login_url='/login/')
@permission_required('core.sprint_status_report', raise_exception=True)
def sprint_status_report(request, **kwargs):
    sprint_status_filter = SprintStatusFilter(request.GET, queryset=Deliverable.objects.all())
    sprint_status_list = sprint_status_filter.qs
    sprint = Sprint.objects.get(pk=request.GET.get('sprint')) if request.GET.get('sprint') else None

    if not request.GET.get('sprint', False):
        sprint_status_list = []

    return render(request, 'core/sprint/sprint_status.html', {
        'sprint_status': sprint_status_list,
        'filter': sprint_status_filter,
        'sprint': sprint
    })


@login_required(login_url='/login/')
@permission_required('core.sprint_status_report_download', raise_exception=True)
def sprint_status_report_download(request, pk, **kwargs):
    sprint_status_list = Deliverable.objects.filter(sprint_id=pk)
    sprint = Sprint.objects.get(pk=pk)

    return PDFRender.render('core/sprint/sprint_status_pdf.html', {
        'sprint_status_list': sprint_status_list,
        'sprint_name': sprint.name
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
            form.save()
            return redirect('sprint_list', permanent=True)
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
        form.save()
        return redirect('sprint_list')
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
