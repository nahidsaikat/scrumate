from datetime import datetime
from django.forms import ModelForm, Textarea, DateInput, HiddenInput, PasswordInput, TextInput
from django_select2.forms import ModelSelect2Widget, Select2Widget
from scrumate.people.models import Department, Designation, Employee, Client
from scrumate.people.choices import PartyTitle, PartyType, PartySubType, PartyGender


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
        exclude = ('rank', )
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
        exclude = ('address_line_3', 'address_line_4', 'nick_name', 'code', 'title')
        widgets = {
            'full_name': HiddenInput(),
            'password': PasswordInput(),
            'title': Select2Widget(choices=PartyTitle.choices),
            'type': Select2Widget(choices=PartyType.choices),
            'gender': Select2Widget(choices=PartyGender.choices),
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
                  'sub_type', 'address_line_1', 'address_line_2']
        exclude = ('address_line_3', 'address_line_4', 'nick_name', 'code', 'title')
        widgets = {
            'full_name': HiddenInput(),
            'type': Select2Widget(choices=PartyType.choices),
            'sub_type': Select2Widget(choices=PartySubType.choices),
        }

    def clean_full_name(self):
        return self.data['first_name'] + ' ' + self.data['last_name']
