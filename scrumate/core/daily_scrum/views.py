from datetime import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect, reverse

from scrumate.core.filters import DailyScrumFilter
from scrumate.core.forms import DeliverableForm
from scrumate.core.models import Deliverable


@login_required(login_url='/login/')
def daily_scrum_entry(request, **kwargs):
    today = datetime.today().date()
    can_assign_dev = request.user.has_perm('assign_deliverable')
    if can_assign_dev:
        queryset = Deliverable.objects.filter(sprint__start_date__lte=today, sprint__end_date__gte=today).order_by('-id')
    elif hasattr(request.user, 'employee'):
        queryset = Deliverable.objects.filter(assign_date=today,
                                              assignee=getattr(request.user, 'employee')).order_by('-id')
    else:
        queryset = None

    deliverable_filter = DailyScrumFilter(request.GET, queryset=queryset)
    deliverable_list = deliverable_filter.qs
    page = request.GET.get('page', 1)

    paginator = Paginator(deliverable_list, settings.PAGE_SIZE)
    try:
        daily_scrums = paginator.page(page)
    except PageNotAnInteger:
        daily_scrums = paginator.page(1)
    except EmptyPage:
        daily_scrums = paginator.page(paginator.num_pages)

    return render(request, 'core/daily_scrum_list.html', {
        'hide': True, 'daily_scrums': daily_scrums, 'filter': deliverable_filter, 'can_assign_dev': can_assign_dev
    })


@login_required(login_url='/login/')
@permission_required('core.assign_deliverable', raise_exception=True)
def assign_dev(request, deliverable_id, **kwargs):
    instance = get_object_or_404(Deliverable, pk=deliverable_id)
    form = DeliverableForm(request.POST or None, instance=instance)

    if request.POST:
        assignee = request.POST.get('assignee')
        instance.assignee_id = assignee
        instance.save()
        return redirect('daily_scrum')

    return render(request, 'includes/single_field.html', {
        'hide': True,
        'field': form.visible_fields()[6],
        'title': 'Assign Dev',
        'url': reverse('daily_scrum'),
        'base_template': 'index.html'
    })


@login_required(login_url='/login/')
@permission_required('core.set_actual_hour', raise_exception=True)
def set_actual_hour(request, deliverable_id, **kwargs):
    return change_actual_hour(deliverable_id, request)


@login_required(login_url='/login/')
@permission_required('core.update_actual_hour', raise_exception=True)
def update_actual_hour(request, deliverable_id, **kwargs):
    return change_actual_hour(deliverable_id, request)


def change_actual_hour(deliverable_id, request):
    instance = get_object_or_404(Deliverable, id=deliverable_id)
    form = DeliverableForm(request.POST or None, instance=instance)
    if request.POST:
        actual_hour = request.POST.get('estimated_hour')
        instance.actual_hour = actual_hour
        instance.save()
        return redirect('daily_scrum')
    return render(request, 'includes/single_field.html', {
        'hide': True,
        'field': form.visible_fields()[4],
        'title': 'Set Actual Hour',
        'url': reverse('daily_scrum'),
        'base_template': 'index.html'
    })
