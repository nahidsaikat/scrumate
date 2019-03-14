from django.forms import ModelForm, Textarea

from .models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        # fields = ['name', 'description']
        fields = '__all__'
        widgets = {
            'description': Textarea(attrs={'cols': 25, 'rows': 3}),
        }

