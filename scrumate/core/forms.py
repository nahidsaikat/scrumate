from django.forms import ModelForm, Textarea, DateInput, TextInput
from django_select2.forms import ModelSelect2Widget, Select2Widget

from scrumate.core.deliverable.choices import DeliverableStatus
from scrumate.core.models import Project, Release, UserStory, Sprint, Issue, Task, Deliverable, DailyScrum
from scrumate.people.models import Employee


class DailyScrumForm(ModelForm):
    class Meta:
        model = DailyScrum
        fields = '__all__'
        exclude = ('project', 'release', 'user_story', 'task', 'issue', 'actual_hour')
        widgets = {
            'estimated_hour': TextInput(attrs={'readonly': True}),
            'comment': Textarea(attrs={'cols': 25, 'rows': 3}),
            'entry_date': DateInput(attrs={'type': 'date'}),
            'project': ModelSelect2Widget(model=Project, search_fields=['name__icontains']),
            'release': ModelSelect2Widget(model=Release, search_fields=['name__icontains'],
                                          dependent_fields={'project': 'project'}, max_results=500),
            'user_story': ModelSelect2Widget(model=UserStory, search_fields=['summary__icontains'],
                                             dependent_fields={'release': 'release'}, max_results=500),
            'task': ModelSelect2Widget(model=Task, search_fields=['name__icontains'],
                                       dependent_fields={'user_story': 'user_story'}, max_results=500),
            'issue': ModelSelect2Widget(model=Issue, search_fields=['name__icontains'], max_results=500),
            'deliverable': ModelSelect2Widget(model=Deliverable, search_fields=['name__icontains'],
                                              dependent_fields={'task': 'task'}, max_results=500),
            'sprint': ModelSelect2Widget(model=Sprint, search_fields=['name__icontains'], max_results=500),
            'employee': ModelSelect2Widget(model=Employee, search_fields=['full_name__icontains'], max_results=500),
        }


class IssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = '__all__'
        exclude = ('comment', 'resolve_date', 'approved_by', 'code', 'project')
        widgets = {
            'description': Textarea(attrs={'cols': 25, 'rows': 3}),
            'raise_date': DateInput(attrs={'type': 'date'}),
            'project': ModelSelect2Widget(model=Project, search_fields=['name__icontains']),
            'user_story': ModelSelect2Widget(model=UserStory, search_fields=['summary__icontains'], max_results=500),
            'raised_by': ModelSelect2Widget(model=Employee, search_fields=['full_name__icontains']),
            'approved_by': ModelSelect2Widget(model=Employee, search_fields=['full_name__icontains']),
            'status': Select2Widget(choices=DeliverableStatus.choices),
        }
