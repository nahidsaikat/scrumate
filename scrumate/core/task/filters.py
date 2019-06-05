import django_filters

from scrumate.core.task.models import Task


class TaskFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Name')

    class Meta:
        model = Task
        fields = ['name', 'project', 'category', 'responsible']
