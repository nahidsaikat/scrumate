import django_filters

from scrumate.core.models import Deliverable


class DeliverableFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Name')

    class Meta:
        model = Deliverable
        fields = ['name', 'sprint', 'assignee']
