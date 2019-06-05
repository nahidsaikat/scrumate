from django.forms import ModelForm, DateInput, Textarea
from django_select2.forms import ModelSelect2Widget, Select2Widget

from scrumate.core.deliverable.choices import DeliverableStatus
from scrumate.core.deliverable.models import Deliverable
from scrumate.core.sprint.models import Sprint
from scrumate.core.task.models import Task
from scrumate.general.choices import Priority
from scrumate.people.models import Employee


class DeliverableForm(ModelForm):
    class Meta:
        model = Deliverable
        fields = '__all__'
        exclude = ('assign_date', 'project', 'actual_hour')
        widgets = {
            'description': Textarea(attrs={'cols': 25, 'rows': 3}),
            'assign_date': DateInput(attrs={'type': 'date'}),
            'release_date': DateInput(attrs={'type': 'date'}),
            'task': ModelSelect2Widget(model=Task, search_fields=['name__icontains']),
            'sprint': ModelSelect2Widget(model=Sprint, search_fields=['name__icontains']),
            'assignee': ModelSelect2Widget(model=Employee, search_fields=['full_name__icontains']),
            'priority': Select2Widget(choices=Priority.choices),
            'status': Select2Widget(choices=DeliverableStatus.choices),
        }
