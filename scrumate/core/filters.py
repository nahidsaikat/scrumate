import django_filters
from django.forms import DateInput
from scrumate.core.models import Project, Release, UserStory, Sprint, Issue, Task, Deliverable


class SprintFilter(django_filters.FilterSet):

    class Meta:
        model = Sprint
        fields = ['name', 'department']


class TaskFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Name')

    class Meta:
        model = Task
        fields = ['name', 'project', 'category', 'responsible']


class DeliverableFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Name')

    class Meta:
        model = Deliverable
        fields = ['name', 'sprint', 'assignee']


class DailyScrumFilter(django_filters.FilterSet):

    class Meta:
        model = Deliverable
        fields = ['project', 'sprint', 'assignee']


class SprintStatusFilter(django_filters.FilterSet):
    sprint = django_filters.ModelChoiceFilter(queryset=Sprint.objects.all())

    class Meta:
        model = Deliverable
        fields = ['sprint']


class IssueFilter(django_filters.FilterSet):
    raise_date = django_filters.DateFilter(widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Issue
        fields = ['name', 'project', 'raise_date']
