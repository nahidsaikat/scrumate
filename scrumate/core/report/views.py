from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render

from scrumate.core.filters import SprintStatusFilter
from scrumate.core.project.filters import ProjectStatusFilter
from scrumate.core.models import Deliverable, Sprint, Release, Project
from scrumate.general.pdf_render import PDFRender


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
@permission_required('core.project_status_report', raise_exception=True)
def project_status_report(request, **kwargs):
    project_status_filter = ProjectStatusFilter(request.GET, queryset=Release.objects.all())
    release_list = project_status_filter.qs
    project = Project.objects.get(pk=request.GET.get('project')) if request.GET.get('project') else None

    if not request.GET.get('project', False):
        release_list = []

    return render(request, 'core/projects/project_status.html', {
        'release_list': release_list,
        'filter': project_status_filter,
        'project': project
    })


@login_required(login_url='/login/')
@permission_required('core.project_status_report_download', raise_exception=True)
def project_status_report_download(request, project_id, **kwargs):
    release_list = Release.objects.filter(project_id=project_id)
    project = Project.objects.get(pk=project_id)

    return PDFRender.render('core/projects/project_status_pdf.html', {
        'release_list': release_list,
        'project_name': project.name
    })
