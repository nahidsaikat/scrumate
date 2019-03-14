from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from .models import Project
from .filters import ProjectFilter
from .forms import ProjectForm


@login_required(login_url='/login/')
def index(request, **kwargs):
    return render(request, 'index.html')


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

    return render(request, 'projects/project_list.html', {'projects': projects, 'filter': project_filter})

@login_required(login_url='/login/')
def project_add(request, **kwargs):
    form = ProjectForm()
    return render(request, 'projects/project_add.html', {'form': form})

