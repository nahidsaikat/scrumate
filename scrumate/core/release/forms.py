from django.forms import ModelForm, Textarea, DateInput
from django_select2.forms import ModelSelect2Widget

from scrumate.core.models import Release, Project
from scrumate.people.models import Employee


class ReleaseForm(ModelForm):
    class Meta:
        model = Release
        fields = '__all__'
        exclude = ('release_log', 'comment', 'delivery_date', 'created_by', 'approved_by', 'project')
        widgets = {
            'description': Textarea(attrs={'cols': 25, 'rows': 3}),
            'release_date': DateInput(attrs={'type': 'date'}),
            'delivery_date': DateInput(attrs={'type': 'date'}),
            'project': ModelSelect2Widget(model=Project, search_fields=['name__icontains']),
            'created_by': ModelSelect2Widget(model=Employee, search_fields=['full_name__icontains']),
            'approved_by': ModelSelect2Widget(model=Employee, search_fields=['full_name__icontains']),
        }
