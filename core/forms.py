from django.forms import ModelForm, Textarea, DateInput, HiddenInput
from django_select2.forms import ModelSelect2Widget, Select2Widget
from .models import Project, Release, UserStory, Sprint, Issue, Department, Designation, Employee, Client, Task, \
    Deliverable, DailyScrum
from .choices import PROJECT_TYPE_CHOICES, PROJECT_STATUS_CHOICES, PARTY_TITLE_CHOICES, PARTY_TYPE_CHOICES, \
    PARTY_SUBTYPE_CHOICES, PARTY_GENDER_CHOICES, USERSTORY_STATUS_CHOICES, SPRINT_STATUS_CHOICES, CATEGORY_CHOICES, \
    PRIORITY_CHOICES, TASK_STATUS_CHOICES, DELIVERABLE_STATUS_CHOICES


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'description': Textarea(attrs={'cols': 25, 'rows': 3}),
            'entry_date': DateInput(attrs={'type': 'date'}),
            'type': Select2Widget(choices=PROJECT_TYPE_CHOICES),
            'status': Select2Widget(choices=PROJECT_STATUS_CHOICES),
            'client': ModelSelect2Widget(model=Client, search_fields=['full_name__icontains']),
        }


class ReleaseForm(ModelForm):
    class Meta:
        model = Release
        fields = '__all__'
        exclude = ('release_log', 'comment')
        widgets = {
            'description': Textarea(attrs={'cols': 25, 'rows': 3}),
            'release_date': DateInput(attrs={'type': 'date'}),
            'delivery_date': DateInput(attrs={'type': 'date'}),
            'project': ModelSelect2Widget(model=Project, search_fields=['name__icontains']),
            'created_by': ModelSelect2Widget(model=Employee, search_fields=['full_name__icontains']),
            'approved_by': ModelSelect2Widget(model=Employee, search_fields=['full_name__icontains']),
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
            'end_date': DateInput(attrs={'type': 'date'}),
            'project': ModelSelect2Widget(model=Project, search_fields=['name__icontains']),
            'release': ModelSelect2Widget(model=Release, search_fields=['name__icontains'],
                                  dependent_fields={'project': 'project'}, max_results=500),
            'analysed_by': ModelSelect2Widget(model=Employee, search_fields=['full_name__icontains']),
            'approved_by': ModelSelect2Widget(model=Employee, search_fields=['full_name__icontains']),
            'status': Select2Widget(choices=USERSTORY_STATUS_CHOICES),
        }


class SprintForm(ModelForm):
    class Meta:
        model = Sprint
        fields = '__all__'
        exclude = ('day_wise_label', )
        widgets = {
            'description': Textarea(attrs={'cols': 25, 'rows': 3}),
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
            'department': ModelSelect2Widget(model=Department, search_fields=['name__icontains']),
            'status': Select2Widget(choices=SPRINT_STATUS_CHOICES),
        }


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        exclude = ()
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
            'category': Select2Widget(choices=CATEGORY_CHOICES),
            'priority': Select2Widget(choices=PRIORITY_CHOICES),
            'status': Select2Widget(choices=TASK_STATUS_CHOICES),
        }


class DeliverableForm(ModelForm):
    class Meta:
        model = Deliverable
        fields = '__all__'
        exclude = ()
        widgets = {
            'description': Textarea(attrs={'cols': 25, 'rows': 3}),
            'assign_date': DateInput(attrs={'type': 'date'}),
            'release_date': DateInput(attrs={'type': 'date'}),
            'task': ModelSelect2Widget(model=Task, search_fields=['name__icontains']),
            'sprint': ModelSelect2Widget(model=Sprint, search_fields=['name__icontains']),
            'assignee': ModelSelect2Widget(model=Employee, search_fields=['full_name__icontains']),
            'priority': Select2Widget(choices=PRIORITY_CHOICES),
            'status': Select2Widget(choices=DELIVERABLE_STATUS_CHOICES),
        }


class DailyScrumForm(ModelForm):
    class Meta:
        model = DailyScrum
        fields = '__all__'
        exclude = ()
        widgets = {
            'comment': Textarea(attrs={'cols': 25, 'rows': 3}),
            'entry_date': DateInput(attrs={'type': 'date'}),
            'project': ModelSelect2Widget(model=Project, search_fields=['name__icontains']),
            'release': ModelSelect2Widget(model=Release, search_fields=['name__icontains'],
                                          dependent_fields={'project': 'project'}, max_results=500),
            'user_story': ModelSelect2Widget(model=UserStory, search_fields=['summary__icontains'],
                                             dependent_fields={'release': 'release'}, max_results=500),
            'task': ModelSelect2Widget(model=Task, search_fields=['name__icontains'],
                                       dependent_fields={'user_story': 'user_story'}, max_results=500),
            'deliverable': ModelSelect2Widget(model=Deliverable, search_fields=['name__icontains'],
                                              dependent_fields={'task': 'task'}, max_results=500),
            'sprint': ModelSelect2Widget(model=Sprint, search_fields=['name__icontains']),
            'employee': ModelSelect2Widget(model=Employee, search_fields=['full_name__icontains']),
        }


class IssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = '__all__'
        exclude = ('comment', 'resolve_date')
        widgets = {
            'description': Textarea(attrs={'cols': 25, 'rows': 3}),
            'raise_date': DateInput(attrs={'type': 'date'}),
            'project': ModelSelect2Widget(model=Project, search_fields=['name__icontains']),
            'user_story': ModelSelect2Widget(model=UserStory, search_fields=['summary__icontains'],
                                             dependent_fields={'project': 'project'}, max_results=500),
            'raised_by': ModelSelect2Widget(model=Employee, search_fields=['full_name__icontains']),
            'approved_by': ModelSelect2Widget(model=Employee, search_fields=['full_name__icontains']),
        }


class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = '__all__'
        widgets = {
            'description': Textarea(attrs={'cols': 25, 'rows': 3}),
        }


class DesignationForm(ModelForm):
    class Meta:
        model = Designation
        fields = '__all__'
        widgets = {
            'description': Textarea(attrs={'cols': 25, 'rows': 3}),
            'department': ModelSelect2Widget(model=Department, search_fields=['name__icontains']),
            'parent': ModelSelect2Widget(model=Designation, search_fields=['name__icontains'],
                                         dependent_fields={'department': 'department'}),
        }


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['title', 'full_name', 'first_name', 'last_name', 'nick_name', 'email', 'phone', 'gender', 'code', 'type',
                  'department', 'designation', 'username', 'password', 'address_line_1', 'address_line_2']
        exclude = ('address_line_3', 'address_line_4')
        widgets = {
            'full_name': HiddenInput(),
            'title': Select2Widget(choices=PARTY_TITLE_CHOICES),
            'type': Select2Widget(choices=PARTY_TYPE_CHOICES),
            'gender': Select2Widget(choices=PARTY_GENDER_CHOICES),
            'department': ModelSelect2Widget(model=Department, search_fields=['name__icontains']),
            'designation': ModelSelect2Widget(model=Designation, search_fields=['name__icontains'],
                                              dependent_fields={'department': 'department'}),
        }

    def clean_full_name(self):
        return self.data['first_name'] + ' ' + self.data['last_name']


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['title', 'full_name', 'first_name', 'last_name', 'nick_name', 'email', 'phone', 'code', 'type',
                  'sub_type', 'username', 'password', 'address_line_1', 'address_line_2']
        exclude = ('address_line_3', 'address_line_4')
        widgets = {
            'full_name': HiddenInput(),
            'type': Select2Widget(choices=PARTY_TYPE_CHOICES),
            'sub_type': Select2Widget(choices=PARTY_SUBTYPE_CHOICES),
        }

    def clean_full_name(self):
        return self.data['first_name'] + ' ' + self.data['last_name']
