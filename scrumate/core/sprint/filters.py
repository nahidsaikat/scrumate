import django_filters

from scrumate.core.models import Sprint


class SprintFilter(django_filters.FilterSet):

    class Meta:
        model = Sprint
        fields = ['name', 'department']
