from django.db import models
from django.contrib.auth import get_user_model
from .choices import PROJECT_STATUS_CHOICES, PROJECT_TYPE_CHOICES, USERSTORY_STATUS_CHOICES, SPRINT_STATUS_CHOICES, \
    COLUMN_CHOICES, CATEGORY_CHOICES, TASK_CHOICES

User = get_user_model()


class Priority(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    description = models.TextField(default='')

class Label(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    description = models.TextField(default='')


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)
    activity_text = models.TextField(default='')
    activity_data = models.TextField(default='')


class Dashboard(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)


class Portlet(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    html_template = models.CharField(max_length=100)
    data_url = models.CharField(max_length=100)


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


class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    description = models.TextField(default='')
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, default=None, null=True)


class Designation(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    description = models.TextField(default='')
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, default=None, null=True)
    department_id = models.ForeignKey(Department, on_delete=models.SET_NULL, default=None, null=True)
    rank = models.IntegerField(default=None)


class ProjectType(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(default='')


class Project(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(default='')
    type = models.IntegerField(choices=PROJECT_TYPE_CHOICES, default=1)
    status = models.IntegerField(choices=PROJECT_STATUS_CHOICES, default=1)
    client = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)
    entry_date = models.DateField(default=None)


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

