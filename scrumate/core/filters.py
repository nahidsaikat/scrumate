import django_filters
from django.forms import DateInput
from django_select2.forms import Select2Widget
from scrumate.core.models import Project, Release, UserStory, Sprint, Issue, Task, Deliverable


class ProjectFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Name')

    class Meta:
        model = Project
        fields = ['name']


class ProjectStatusFilter(django_filters.FilterSet):
    project = django_filters.ModelChoiceFilter(queryset=Project.objects.all())

    class Meta:
        model = Release
        fields = ['project']


class ReleaseFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Name')

    class Meta:
        model = Release
        fields = ['name']


class UserStoryFilter(django_filters.FilterSet):
    # project = django_filters.ModelChoiceFilter(queryset=UserStory.objects.all())

    class Meta:
        model = UserStory
        fields = ['project', 'release']


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
