import django_filters
from django.forms import DateInput
from scrumate.core.models import Project, Release, UserStory, Sprint, Issue, Task, Deliverable


class IssueFilter(django_filters.FilterSet):
    raise_date = django_filters.DateFilter(widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Issue
        fields = ['name', 'project', 'raise_date']
