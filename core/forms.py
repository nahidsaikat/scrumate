from django.forms import ModelForm, Textarea, DateInput, HiddenInput, ModelChoiceField
from django_select2.forms import ModelSelect2Widget
from .models import Project, Release, UserStory, Sprint, Issue, Department, Designation, Employee, Client, Task, \
    Deliverable, DailyScrum


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
    release = ModelChoiceField(queryset=Release.objects.all(),
        widget=ModelSelect2Widget(model=Release, search_fields=['name__icontains'],
                                  dependent_fields={'project': 'project'}, max_results=500)
    )

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


class SprintForm(ModelForm):
    class Meta:
        model = Sprint
        fields = '__all__'
        exclude = ('day_wise_label', )
        widgets = {
            'description': Textarea(attrs={'cols': 25, 'rows': 3}),
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'})
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
        }


class DailyScrumForm(ModelForm):
    class Meta:
        model = DailyScrum
        fields = '__all__'
        exclude = ()
        widgets = {
            'comment': Textarea(attrs={'cols': 25, 'rows': 3}),
            'entry_date': DateInput(attrs={'type': 'date'}),
        }


class IssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = '__all__'
        exclude = ('comment', 'resolve_date')
        widgets = {
            'description': Textarea(attrs={'cols': 25, 'rows': 3}),
            'raise_date': DateInput(attrs={'type': 'date'}),
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
        }


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['title', 'full_name', 'first_name', 'last_name', 'nick_name', 'email', 'phone', 'gender', 'code', 'type',
                  'department', 'designation', 'username', 'password', 'address_line_1', 'address_line_2']
        exclude = ('address_line_3', 'address_line_4')
        widgets = {
            'full_name': HiddenInput()
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
            'full_name': HiddenInput()
        }

    def clean_full_name(self):
        return self.data['first_name'] + ' ' + self.data['last_name']
