from django.forms import ModelForm, Textarea, DateInput
from django_select2.forms import ModelSelect2Widget, Select2Widget

from scrumate.core.release.models import Release
from scrumate.core.project.models import Project
from scrumate.core.user_story.models import UserStory
from scrumate.core.user_story.choices import UserStoryStatus
from scrumate.people.models import Employee


class UserStoryForm(ModelForm):
    class Meta:
        model = UserStory
        fields = '__all__'
        exclude = ('description', 'comment', 'code', 'analysed_by', 'approved_by', 'project')
        widgets = {
            'summary': Textarea(attrs={'cols': 25, 'rows': 1}),
            'details': Textarea(attrs={'cols': 25, 'rows': 3}),
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
            'project': ModelSelect2Widget(model=Project, search_fields=['name__icontains']),
            'release': ModelSelect2Widget(model=Release, search_fields=['name__icontains'],
                                  dependent_fields={'project': 'project'}, max_results=500),
            'analysed_by': ModelSelect2Widget(model=Employee, search_fields=['full_name__icontains']),
            'approved_by': ModelSelect2Widget(model=Employee, search_fields=['full_name__icontains']),
            'status': Select2Widget(choices=UserStoryStatus.choices),
        }
