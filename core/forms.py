from django.forms import ModelForm, Textarea, DateInput, CharField

from .models import Project, Release, UserStory


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'description': Textarea(attrs={'cols': 25, 'rows': 3}),
            'entry_date': DateInput(attrs={'type': 'date'})
        }


class ReleaseForm(ModelForm):
    class Meta:
        model = Release
        fields = '__all__'
        exclude = ('release_log', 'comment')
        widgets = {
            'description': Textarea(attrs={'cols': 25, 'rows': 3}),
            'release_date': DateInput(attrs={'type': 'date'}),
            'delivery_date': DateInput(attrs={'type': 'date'})
        }


class UserStoryForm(ModelForm):
    class Meta:
        model = UserStory
        fields = '__all__'
        exclude = ('description', 'comment')
        widgets = {
            'summary': Textarea(attrs={'cols': 25, 'rows': 1}),
            'details': Textarea(attrs={'cols': 25, 'rows': 3}),
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'})
        }
