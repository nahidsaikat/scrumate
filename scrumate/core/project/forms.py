from django.forms import ModelForm, PasswordInput, Textarea, DateInput
from django_select2.forms import Select2Widget, ModelSelect2Widget

from scrumate.core.models import Project
from scrumate.core.project.choices import ProjectStatus, ProjectType
from scrumate.people.models import Client


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ('last_sync_time', )
        widgets = {
            'git_password': PasswordInput(),
            'description': Textarea(attrs={'cols': 25, 'rows': 3}),
            'entry_date': DateInput(attrs={'type': 'date'}),
            'type': Select2Widget(choices=ProjectType.choices),
            'status': Select2Widget(choices=ProjectStatus.choices),
            'client': ModelSelect2Widget(model=Client, search_fields=['full_name__icontains']),
        }
