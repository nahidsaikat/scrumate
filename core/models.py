from django.db import models
from django.contrib.auth import get_user_model
from .choices import PROJECT_STATUS_CHOICES, PROJECT_TYPE_CHOICES, USERSTORY_STATUS_CHOICES, SPRINT_STATUS_CHOICES, \
    COLUMN_CHOICES, CATEGORY_CHOICES, TASK_CHOICES, DELIVERABLE_STATUS_CHOICES, PARTY_TYPE_CHOICES, PARTY_GENDER_CHOICES

User = get_user_model()


class Priority(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    description = models.TextField(default='')
    
    def __str__(self):
        return self.name


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
    column = models.IntegerField(choices=COLUMN_CHOICES, default=1)
    height = models.DecimalField(default=50, decimal_places=2, max_digits=15)
    width = models.DecimalField(default=100, decimal_places=2, max_digits=15)


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
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, default=None, null=True)

    def __str__(self):
        return self.name


class Designation(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    description = models.TextField(default='')
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, default=None, null=True)
    department_id = models.ForeignKey(Department, on_delete=models.SET_NULL, default=None, null=True)
    rank = models.IntegerField(default=None)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(default='')
    type = models.IntegerField(choices=PROJECT_TYPE_CHOICES, default=1)
    status = models.IntegerField(choices=PROJECT_STATUS_CHOICES, default=1)
    client = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)
    entry_date = models.DateField(default=None)

    def __str__(self):
        return self.name


class Release(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(default='')
    version = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    release_date = models.DateField(default=None)
    delivery_date = models.DateField(default=None)
    release_log = models.TextField(default=None)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, related_name='created_releases')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, related_name='approved_releases')
    comment = models.TextField(default='')

    def __str__(self):
        return self.name


class UserStory(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=None)
    release = models.ForeignKey(Release, on_delete=models.CASCADE, default=None)
    summary = models.TextField(default='')
    details = models.TextField(default='')
    code = models.CharField(max_length=100, default='')
    start_date = models.DateField(default=None)
    end_date = models.DateField(default=None)
    description = models.TextField(default='')
    analysed_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, related_name='analysed_user_stories')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, related_name='approved_user_stories')
    status = models.IntegerField(choices=USERSTORY_STATUS_CHOICES, default=1)
    comment = models.TextField(default='')

    def __str__(self):
        return self.summary


class Issue(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    description = models.TextField(default='')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, default=None, null=True)
    user_story = models.ForeignKey(UserStory, on_delete=models.SET_NULL, default=None, null=True)
    raise_date = models.DateField(default=None)
    resolve_date = models.DateField(default=None)
    raised_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, related_name='raised_issues')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, related_name='approved_issues')
    comment = models.TextField(default='')

    def __str__(self):
        return self.name


class Sprint(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    description = models.TextField(default='')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, default=None, null=True)
    start_date = models.DateField(default=None)
    end_date = models.DateField(default=None)
    day_wise_label = models.TextField(default='')
    status = models.IntegerField(choices=SPRINT_STATUS_CHOICES, default=1)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, default=None, null=True)
    user_story = models.ForeignKey(UserStory, on_delete=models.CASCADE)
    sprint = models.ForeignKey(Sprint, on_delete=models.SET_NULL, default=None, null=True)
    issue = models.ForeignKey(Issue, on_delete=models.SET_NULL, default=None, null=True)
    category = models.IntegerField(choices=CATEGORY_CHOICES, default=1)
    responsible = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, related_name='responsible_tasks')
    estimation = models.DecimalField(default=0.0, decimal_places=2, max_digits=15)
    start_date = models.DateField(default=None)
    end_date = models.DateField(default=None)
    priority = models.ForeignKey(Priority, on_delete=models.SET_NULL, default=None, null=True)
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, related_name='assigned_tasks')
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, related_name='assigned_by_tasks')
    assign_date = models.DateField(default=None)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, related_name='approved_by_tasks')
    approved_date = models.DateField(default=None)
    status = models.IntegerField(choices=TASK_CHOICES, default=1)
    parent_task = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, default=None, null=True)

    def __str__(self):
        return self.name


class Deliverable(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, default=None, null=True)
    release = models.ForeignKey(Release, on_delete=models.SET_NULL, default=None, null=True)
    user_story = models.ForeignKey(UserStory, on_delete=models.SET_NULL, default=None, null=True)
    sprint = models.ForeignKey(Sprint, on_delete=models.SET_NULL, default=None, null=True)
    estimated_hour = models.DecimalField(default=0.0, decimal_places=2, max_digits=15)
    priority = models.ForeignKey(Priority, on_delete=models.SET_NULL, default=None, null=True)
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)
    assign_date = models.DateField(default=None)
    release_date = models.DateField(default=None)
    status = models.IntegerField(choices=DELIVERABLE_STATUS_CHOICES, default=1)

    def __str__(self):
        return self.name


class DailyScrum(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, default=None, null=True)
    release = models.ForeignKey(Release, on_delete=models.SET_NULL, default=None, null=True)
    user_story = models.ForeignKey(UserStory, on_delete=models.SET_NULL, default=None, null=True)
    sprint = models.ForeignKey(Sprint, on_delete=models.SET_NULL, default=None, null=True)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, default=None, null=True)
    deliverable = models.ForeignKey(Deliverable, on_delete=models.SET_NULL, default=None, null=True)
    entry_date = models.DateField(default=None)
    estimated_hour = models.DecimalField(default=0.0, decimal_places=2, max_digits=15)
    actual_hour = models.DecimalField(default=0.0, decimal_places=2, max_digits=15)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)
    comment = models.TextField(default='')

    def __str__(self):
        return self.project.name + ' ' + self.task.name


class OverTime(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, default=None, null=True)
    work_date = models.DateField(default=None)
    description = models.TextField(default='')
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, related_name='assignee_over_times')
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, related_name='assigned_by_over_times')
    comment = models.TextField(default='')
    status = models.IntegerField(choices=DELIVERABLE_STATUS_CHOICES, default=1)


class Party(models.Model):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    nick_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    type = models.IntegerField(choices=PARTY_TYPE_CHOICES)
    sub_type = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)
    address_line_1 = models.CharField(max_length=100, null=True)
    address_line_2 = models.CharField(max_length=100, null=True, blank=True)
    address_line_3 = models.CharField(max_length=100, null=True, blank=True)
    address_line_4 = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.full_name


class Employee(Party):
    gender = models.IntegerField(choices=PARTY_GENDER_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, default=None, null=True)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, default=None, null=True)
