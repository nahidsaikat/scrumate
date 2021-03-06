import django_filters

from scrumate.core.deliverable.models import Deliverable


class DailyScrumFilter(django_filters.FilterSet):

    class Meta:
        model = Deliverable
        fields = ['project', 'sprint', 'assignee']
