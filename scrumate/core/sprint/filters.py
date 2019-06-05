import django_filters

from scrumate.core.sprint.models import Sprint
from scrumate.core.deliverable.models import Deliverable


class SprintFilter(django_filters.FilterSet):

    class Meta:
        model = Sprint
        fields = ['name', 'department']


class SprintStatusFilter(django_filters.FilterSet):
    sprint = django_filters.ModelChoiceFilter(queryset=Sprint.objects.all())

    class Meta:
        model = Deliverable
        fields = ['sprint']
