import django_filters
from .models import Project, Release, UserStory


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
