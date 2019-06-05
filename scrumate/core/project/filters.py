import django_filters

from scrumate.core.project.models import Project
from scrumate.core.release.models import Release


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
