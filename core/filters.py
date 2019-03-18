import django_filters
from django.forms import DateInput
from .models import Project, Release, UserStory, Sprint, Issue


class ProjectFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Name')

    class Meta:
        model = Project
        fields = ['name']


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


class IssueFilter(django_filters.FilterSet):
    raise_date = django_filters.DateFilter(widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Issue
        fields = ['name', 'project', 'raise_date']

