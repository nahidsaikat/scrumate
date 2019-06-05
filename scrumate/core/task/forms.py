from django.forms import ModelForm, DateInput
from django_select2.forms import ModelSelect2Widget, Select2Widget

from scrumate.core.task.models import Task
from scrumate.core.task.choices import TaskStatus, Category
from scrumate.core.project.models import Project
from scrumate.core.user_story.models import UserStory
from scrumate.core.issue.models import Issue
from scrumate.core.release.models import Release
from scrumate.general.choices import Priority
from scrumate.people.models import Employee


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        exclude = ('project', 'release', 'code', 'category', 'responsible', 'assigned_by', 'assign_date', 'approved_by',
                   'approved_date', 'parent_task', 'estimation')
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
            'assign_date': DateInput(attrs={'type': 'date'}),
            'approved_date': DateInput(attrs={'type': 'date'}),
            'project': ModelSelect2Widget(model=Project, search_fields=['name__icontains']),
            'release': ModelSelect2Widget(model=Release, search_fields=['name__icontains'],
                                          dependent_fields={'project': 'project'}, max_results=500),
            'user_story': ModelSelect2Widget(model=UserStory, search_fields=['summary__icontains'],
                                             dependent_fields={'release': 'release'}, max_results=500),
            'issue': ModelSelect2Widget(model=Issue, search_fields=['name__icontains']),
            'responsible': ModelSelect2Widget(model=Employee, search_fields=['full_name__icontains']),
            'assignee': ModelSelect2Widget(model=Employee, search_fields=['full_name__icontains']),
            'assigned_by': ModelSelect2Widget(model=Employee, search_fields=['full_name__icontains']),
            'approved_by': ModelSelect2Widget(model=Employee, search_fields=['full_name__icontains']),
            'parent_task': ModelSelect2Widget(model=Task, search_fields=['name__icontains']),
            'category': Select2Widget(choices=Category.choices),
            'priority': Select2Widget(choices=Priority.choices),
            'status': Select2Widget(choices=TaskStatus.choices),
        }
