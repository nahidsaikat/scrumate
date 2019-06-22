from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from scrumate.core.project.models import Project
from scrumate.people.filters import DepartmentFilter, DesignationFilter, EmployeeFilter, ClientFilter
from scrumate.people.forms import DepartmentForm, DesignationForm, EmployeeForm, ClientForm
from scrumate.people.models import Department, Designation, Employee, Client
from scrumate.general.views import HistoryList

User = get_user_model()


@login_required(login_url='/login/')
def profile(request, **kwargs):
    employee = request.user.employee if request.user and hasattr(request.user, 'employee') else None
    return render(request, 'people/profile.html', {'employee': employee})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'people/change_password.html', {'form': form})


@login_required(login_url='/login/')
def department_list(request, **kwargs):
    department_filter = DepartmentFilter(request.GET, queryset=Department.objects.all())
    department_list = department_filter.qs
    page = request.GET.get('page', 1)

    paginator = Paginator(department_list, settings.PAGE_SIZE)
    try:
        departments = paginator.page(page)
    except PageNotAnInteger:
        departments = paginator.page(1)
    except EmptyPage:
        departments = paginator.page(paginator.num_pages)

    return render(request, 'people/department_list.html', {'departments': departments, 'filter': department_filter})


@login_required(login_url='/login/')
def department_add(request, **kwargs):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department_list', permanent=True)
    else:
        form = DepartmentForm()
    title = 'New Department'
    return render(request, 'people/common_people_add.html', {'form': form, 'title': title, 'list_url_name': 'department_list'})


@login_required(login_url='/login/')
def department_edit(request, pk, **kwargs):
    instance = get_object_or_404(Department, id=pk)
    form = DepartmentForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('department_list')
    title = 'Edit Department'
    return render(request, 'people/common_people_add.html', {'form': form, 'title': title, 'list_url_name': 'department_list'})


@login_required(login_url='/login/')
def designation_list(request, **kwargs):
    designation_filter = DesignationFilter(request.GET, queryset=Designation.objects.all())
    designation_list = designation_filter.qs
    page = request.GET.get('page', 1)

    paginator = Paginator(designation_list, settings.PAGE_SIZE)
    try:
        designations = paginator.page(page)
    except PageNotAnInteger:
        designations = paginator.page(1)
    except EmptyPage:
        designations = paginator.page(paginator.num_pages)

    return render(request, 'people/designation_list.html', {'designations': designations, 'filter': designation_filter})


@login_required(login_url='/login/')
def designation_add(request, **kwargs):
    if request.method == 'POST':
        form = DesignationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('designation_list', permanent=True)
    else:
        form = DesignationForm()
    title = 'New Designation'
    return render(request, 'people/common_people_add.html', {'form': form, 'title': title, 'list_url_name': 'designation_list'})


@login_required(login_url='/login/')
def designation_edit(request, pk, **kwargs):
    instance = get_object_or_404(Designation, id=pk)
    form = DesignationForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('designation_list')
    title = 'Edit Designation'
    return render(request, 'people/common_people_add.html', {'form': form, 'title': title, 'list_url_name': 'designation_list'})


@login_required(login_url='/login/')
def employee_list(request, **kwargs):
    employee_filter = EmployeeFilter(request.GET, queryset=Employee.objects.all())
    employee_list = employee_filter.qs
    page = request.GET.get('page', 1)

    paginator = Paginator(employee_list, settings.PAGE_SIZE)
    try:
        employees = paginator.page(page)
    except PageNotAnInteger:
        employees = paginator.page(1)
    except EmptyPage:
        employees = paginator.page(paginator.num_pages)

    return render(request, 'people/employee_list.html', {'employees': employees, 'filter': employee_filter})


@login_required(login_url='/login/')
def employee_add(request, **kwargs):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email']
            )
            user.save()
            employee = form.save(commit=False)
            if user:
                employee.user = user
            employee.save()

            return redirect('employee_list', permanent=True)
    else:
        form = EmployeeForm()
    title = 'New Employee'
    return render(request, 'people/common_people_add.html', {'form': form, 'title': title, 'list_url_name': 'employee_list'})


@login_required(login_url='/login/')
def employee_edit(request, pk, **kwargs):
    instance = get_object_or_404(Employee, id=pk)
    form = EmployeeForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('employee_list')
    title = 'Edit Employee'
    return render(request, 'people/common_people_add.html', {'form': form, 'title': title, 'list_url_name': 'employee_list'})


@login_required(login_url='/login/')
def client_list(request, **kwargs):
    client_filter = ClientFilter(request.GET, queryset=Client.objects.all())
    client_list = client_filter.qs
    page = request.GET.get('page', 1)

    paginator = Paginator(client_list, settings.PAGE_SIZE)
    try:
        clients = paginator.page(page)
    except PageNotAnInteger:
        clients = paginator.page(1)
    except EmptyPage:
        clients = paginator.page(paginator.num_pages)

    return render(request, 'people/client_list.html', {'clients': clients, 'filter': client_filter})


@login_required(login_url='/login/')
def client_add(request, **kwargs):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list', permanent=True)
    else:
        form = ClientForm()
    title = 'New Client'
    return render(request, 'people/common_people_add.html', {'form': form, 'title': title, 'list_url_name': 'client_list'})


@login_required(login_url='/login/')
def client_edit(request, pk, **kwargs):
    instance = get_object_or_404(Client, id=pk)
    form = ClientForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('client_list')
    title = 'Edit Client'
    return render(request, 'people/common_people_add.html', {'form': form, 'title': title, 'list_url_name': 'client_list'})


class ClientHistoryList(HistoryList):

    def get_client_id(self):
        return self.kwargs.get('pk')

    def get_queryset(self):
        return Client.history.filter(id=self.get_client_id())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = Client.objects.get(pk=self.get_client_id())

        context['title'] = f'History of {client.full_name}'
        context['back_url'] = reverse('client_list')
        context['base_template'] = 'general/index_settings.html'
        return context


class EmployeeHistoryList(HistoryList):

    def get_employee_id(self):
        return self.kwargs.get('pk')

    def get_queryset(self):
        return Employee.history.filter(id=self.get_employee_id())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee = Employee.objects.get(pk=self.get_employee_id())

        context['title'] = f'History of {employee.full_name}'
        context['back_url'] = reverse('employee_list')
        context['base_template'] = 'general/index_settings.html'
        return context
