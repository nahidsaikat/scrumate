from django.forms import ModelForm, Textarea, DateInput
from django_select2.forms import ModelSelect2Widget, Select2Widget

from scrumate.core.deliverable.choices import DeliverableStatus
from scrumate.core.models import Project, UserStory, Issue
from scrumate.people.models import Employee


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
