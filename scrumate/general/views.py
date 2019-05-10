from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url='/login/')
def settings(request, **kwargs):
    employee = request.user.employee if request.user and hasattr(request.user, 'employee') else None
    return render(request, 'index_settings.html', {'employee': employee})


@login_required(login_url='/login/')
def reports(request, **kwargs):
    employee = request.user.employee if request.user and hasattr(request.user, 'employee') else None
    return render(request, 'index_reports.html', {'employee': employee})


@login_required(login_url='/login/')
def sprint(request, **kwargs):
    employee = request.user.employee if request.user and hasattr(request.user, 'employee') else None
    return render(request, 'index_sprint.html', {'employee': employee})


@login_required(login_url='/login/')
def project(request, **kwargs):
    employee = request.user.employee if request.user and hasattr(request.user, 'employee') else None
    return render(request, 'index_project.html', {'employee': employee})

