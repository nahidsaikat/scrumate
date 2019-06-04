import django_filters

from scrumate.core.models import Release


class ReleaseFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Name')

    class Meta:
        model = Release
        fields = ['name']
