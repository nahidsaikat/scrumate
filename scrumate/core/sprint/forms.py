from datetime import datetime

from django.forms import ModelForm, HiddenInput, DateInput, Textarea
from django_select2.forms import ModelSelect2Widget, Select2Widget

from scrumate.core.sprint.models import Sprint
from scrumate.core.sprint.choices import SprintStatus
from scrumate.general.utils import generate_day_wise_label
from scrumate.people.models import Department


class SprintForm(ModelForm):
    class Meta:
        model = Sprint
        fields = '__all__'
        exclude = ('code', 'project')
        widgets = {
            'day_wise_label': HiddenInput(),
            'description': Textarea(attrs={'cols': 25, 'rows': 3}),
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
            'department': ModelSelect2Widget(model=Department, search_fields=['name__icontains']),
            'status': Select2Widget(choices=SprintStatus.choices),
        }

    def clean_day_wise_label(self):
        start_date = datetime.strptime(self.data['start_date'], "%Y-%m-%d").date()
        end_date = datetime.strptime(self.data['end_date'], "%Y-%m-%d").date()
        return generate_day_wise_label(start_date, end_date)
