from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Project


@login_required(login_url='/login/')
def index(request, **kwargs):
    return render(request, 'index.html')


@login_required(login_url='/login/')
def project_list(request, **kwargs):
    project_list = Project.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(project_list, 10)
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)

    return render(request, 'projects/project_list.html', {'projects': projects})
