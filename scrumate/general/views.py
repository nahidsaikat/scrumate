from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url='/login/')
def settings(request, **kwargs):
    employee = request.user.employee if request.user and hasattr(request.user, 'employee') else None
    return render(request, 'index_settings.html', {'employee': employee})

