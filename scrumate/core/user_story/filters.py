import django_filters

from scrumate.core.models import UserStory


class UserStoryFilter(django_filters.FilterSet):
    summary = django_filters.CharFilter(label='Story')

    class Meta:
        model = UserStory
        fields = ['summary', 'release']
