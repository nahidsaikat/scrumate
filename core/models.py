import datetime
from django.db import models
from django.contrib.auth import get_user_model
from .choices import ProjectStatus, ProjectType, UserStoryStatus, SprintStatus, Column, Category, TaskStatus, \
    DeliverableStatus, PartyType, PartyGender, Priority, PartyTitle, PartySubType

User = get_user_model()


class Division(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    description = models.TextField(default='')

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    description = models.TextField(default='')
    # division = models.ForeignKey(Division, on_delete=models.SET_NULL, default=None, null=True)

    def __str__(self):
        return self.name


class Designation(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(default='', null=True, blank=True)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, default=None, null=True)
    rank = models.IntegerField(default=None, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, default=None, null=True, blank=True)

    def __str__(self):
        return self.name


class Party(models.Model):
    title = models.IntegerField(choices=PartyTitle.choices, default=PartyTitle.Mr)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    full_name = models.CharField(max_length=200, blank=True)
    nick_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    address_line_1 = models.CharField(max_length=100, null=True)
    address_line_2 = models.CharField(max_length=100, null=True, blank=True)
    address_line_3 = models.CharField(max_length=100, null=True, blank=True)
    address_line_4 = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.full_name


class Employee(Party):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name='employee')
    type = models.IntegerField(choices=PartyType.choices, default=PartyType.Employee)
    gender = models.IntegerField(choices=PartyGender.choices)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, default=None, null=True)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, default=None, null=True)


class Client(Party):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name='client')
    type = models.IntegerField(choices=PartyType.choices, default=PartyType.Customer)
    sub_type = models.IntegerField(choices=PartySubType, default=PartySubType.Organization)


class Label(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    description = models.TextField(default='')

    def __str__(self):
        return self.name


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)
    activity_text = models.TextField(default='')
    activity_data = models.TextField(default='')


class Dashboard(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ("dev_dashboard", "Can See Dev Dashboard"),
        )


class Portlet(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    html_template = models.CharField(max_length=100)
    data_url = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class DashboardPortlet(models.Model):
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)
    portlet = models.ForeignKey(Portlet, on_delete=models.CASCADE)
    column = models.IntegerField(choices=Column, default=Column.One)
    height = models.DecimalField(default=50, decimal_places=2, max_digits=15)
    width = models.DecimalField(default=100, decimal_places=2, max_digits=15)


class Project(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(default='')
    type = models.IntegerField(choices=ProjectType.choices, default=ProjectType.Public)
    status = models.IntegerField(choices=ProjectStatus.choices, default=1)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, default=None, null=True)
    entry_date = models.DateField("Entry Date", default=datetime.date.today)

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ("update_project_status", "Can Update Status of Project"),
        )


class Release(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(default='', null=True, blank=True)
    version = models.CharField(max_length=100, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    release_date = models.DateField(default=None)
    delivery_date = models.DateField(default=None, null=True, blank=True)
    release_log = models.TextField(default=None, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, related_name='created_releases')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, related_name='approved_releases')
    comment = models.TextField(default='', null=True, blank=True)

    def __str__(self):
        return self.name


class UserStory(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=None)
    release = models.ForeignKey(Release, on_delete=models.CASCADE, default=None)
    summary = models.TextField(default='', verbose_name='Title')
    details = models.TextField(default='', null=True, blank=True)
    code = models.CharField(max_length=100, default='')
    start_date = models.DateField(default=None, null=True, blank=True)
    end_date = models.DateField(default=None, null=True, blank=True)
    description = models.TextField(default='', null=True, blank=True)
    analysed_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name='analysed_user_stories')
    approved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name='approved_user_stories')
    status = models.IntegerField(choices=UserStoryStatus.choices, default=UserStoryStatus.Pending, null=True, blank=True)
    comment = models.TextField(default='', null=True, blank=True)

    def __str__(self):
        return self.summary


class Issue(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    description = models.TextField(default='', blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, default=None, null=True)
    user_story = models.ForeignKey(UserStory, on_delete=models.SET_NULL, default=None, null=True)
    raise_date = models.DateField(default=None)
    resolve_date = models.DateField(default=None, blank=True, null=True)
    raised_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, default=None, blank=True, null=True, related_name='raised_issues')
    approved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, default=None, blank=True, null=True, related_name='approved_issues')
    comment = models.TextField(default='', blank=True, null=True)
    status = models.IntegerField(choices=DeliverableStatus.choices, default=DeliverableStatus.Pending)

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ("update_issue_status", "Can Update Status of Issue"),
        )


class Sprint(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(default='', null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    start_date = models.DateField(default=None, null=True, blank=True)
    end_date = models.DateField(default=None, null=True, blank=True)
    day_wise_label = models.TextField(default='', null=True, blank=True)
    status = models.IntegerField(choices=SprintStatus.choices, default=1, null=True, blank=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, default=None, null=True)
    release = models.ForeignKey(Release, on_delete=models.SET_NULL, default=None, null=True)
    user_story = models.ForeignKey(UserStory, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    category = models.IntegerField(choices=Category.choices, default=Category.Analysis)
    responsible = models.ForeignKey(Employee, on_delete=models.SET_NULL, default=None, null=True, related_name='responsible_tasks')
    estimation = models.DecimalField(default=0.0, decimal_places=2, max_digits=15)
    start_date = models.DateField(default=None)
    end_date = models.DateField(default=None, null=True, blank=True)
    priority = models.IntegerField(choices=Priority.choices, default=Priority.High, null=True)
    assignee = models.ForeignKey(Employee, on_delete=models.SET_NULL, default=None, null=True, related_name='assigned_tasks')
    assigned_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, default=None, null=True, related_name='assigned_by_tasks')
    assign_date = models.DateField(default=None, null=True, blank=True)
    approved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, default=None, null=True, related_name='approved_by_tasks')
    approved_date = models.DateField(default=None, null=True, blank=True)
    status = models.IntegerField(choices=TaskStatus.choices, default=TaskStatus.Pending)
    parent_task = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, default=None, null=True)

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ("update_task_status", "Can Update Status of Task"),
        )


class Deliverable(models.Model):
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, default=None, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(default='', null=True, blank=True)
    sprint = models.ForeignKey(Sprint, on_delete=models.SET_NULL, default=None, null=True)
    estimated_hour = models.DecimalField(default=0.0, decimal_places=2, max_digits=15, null=True, blank=True)
    priority = models.IntegerField(choices=Priority.choices, default=Priority.High, null=True, blank=True)
    assignee = models.ForeignKey(Employee, on_delete=models.SET_NULL, default=None, null=True)
    assign_date = models.DateField(default=None, null=True, blank=True)
    release_date = models.DateField(default=None, null=True, blank=True)
    status = models.IntegerField(choices=DeliverableStatus.choices, default=DeliverableStatus.Pending, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ("update_deliverable_status", "Can Update Status of Deliverable"),
        )


class DailyScrum(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, default=None, null=True)
    release = models.ForeignKey(Release, on_delete=models.SET_NULL, default=None, null=True)
    user_story = models.ForeignKey(UserStory, on_delete=models.SET_NULL, default=None, null=True)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, default=None, null=True)
    deliverable = models.ForeignKey(Deliverable, on_delete=models.SET_NULL, default=None, null=True)
    sprint = models.ForeignKey(Sprint, on_delete=models.SET_NULL, default=None, null=True)
    entry_date = models.DateField(default=None, null=True, blank=True)
    estimated_hour = models.DecimalField(default=0.0, decimal_places=2, max_digits=15, null=True, blank=True)
    actual_hour = models.DecimalField(default=0.0, decimal_places=2, max_digits=15, null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, default=None, null=True)
    comment = models.TextField(default='', null=True, blank=True)

    def __str__(self):
        return self.project.name + ' ' + self.task.name

    class Meta:
        permissions = (
            ("set_actual_hour", "Can Set Actual Hour of Daily Scrum"),
            ("update_actual_hour", "Can Update Actual Hour of Daily Scrum"),
        )


class OverTime(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, default=None, null=True)
    work_date = models.DateField(default=None)
    description = models.TextField(default='')
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, related_name='assignee_over_times')
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, related_name='assigned_by_over_times')
    comment = models.TextField(default='')
    status = models.IntegerField(choices=DeliverableStatus.choices, default=DeliverableStatus.Pending)

