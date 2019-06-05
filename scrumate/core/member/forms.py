from django.forms import ModelForm
from django_select2.forms import ModelSelect2Widget, Select2Widget

from scrumate.core.member.choices import ProjectMemberRole
from scrumate.core.member.models import ProjectMember
from scrumate.core.project.models import Project
from scrumate.people.models import Employee


class ProjectMemberForm(ModelForm):
    class Meta:
        model = ProjectMember
        fields = '__all__'
        exclude = ('project', )
        widgets = {
            'project': ModelSelect2Widget(model=Project, search_fields=['name__icontains']),
            'user': ModelSelect2Widget(model=Employee, search_fields=['full_name__icontains']),
            'role': Select2Widget(choices=ProjectMemberRole.choices),
        }
