import django_filters
from scrumate.people.models import Department, Designation, Employee, Client


class DepartmentFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Name')
    code = django_filters.CharFilter(lookup_expr='icontains', label='Code')

    class Meta:
        model = Department
        fields = ['name', 'code']


class DesignationFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Name')
    code = django_filters.CharFilter(lookup_expr='icontains', label='Code')

    class Meta:
        model = Designation
        fields = ['name', 'code', 'department']


class EmployeeFilter(django_filters.FilterSet):
    full_name = django_filters.CharFilter(lookup_expr='icontains', label='Name')
    code = django_filters.CharFilter(lookup_expr='icontains', label='Code')

    class Meta:
        model = Employee
        fields = ['full_name', 'code', 'department']


class ClientFilter(django_filters.FilterSet):
    full_name = django_filters.CharFilter(lookup_expr='icontains', label='Name')
    code = django_filters.CharFilter(lookup_expr='icontains', label='Code')

    class Meta:
        model = Client
        fields = ['full_name', 'code', 'sub_type']
