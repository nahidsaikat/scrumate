import django_filters
from .models import Project, Release


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
