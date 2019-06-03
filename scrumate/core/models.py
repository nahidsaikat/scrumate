import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum, Q

from scrumate.core.choices import SprintStatus, Column, Category, TaskStatus, \
    DeliverableStatus, Priority
from scrumate.core.project.choices import ProjectStatus, ProjectType, ProjectMemberRole
from scrumate.core.user_story.choices import UserStoryStatus
from scrumate.general.source_control import get_commit_messages
from scrumate.people.models import Employee, Client, Department

User = get_user_model()


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
    status = models.IntegerField(choices=ProjectStatus.choices, default=ProjectStatus.Pending)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    entry_date = models.DateField("Entry Date", default=datetime.date.today)
    git_username = models.CharField(verbose_name='Github Username', max_length=50, null=True, blank=True)
    git_password = models.CharField(verbose_name='Github Password', max_length=50, null=True, blank=True)
    git_repo = models.CharField(verbose_name='Github Repo', max_length=100, null=True, blank=True)
    last_sync_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ("update_project_status", "Can Update Status of Project"),
            ("view_commit_logs", "Can View Commit Logs of Project"),
            ("project_status_report", "Can See Project Status Report"),
            ("project_status_report_download", "Can Download Project Status Report"),
            ("project_members", "Can See Members of a Project"),
            ("assign_deliverable", "Can Assign Deliverables"),
        )

    @property
    def commit_messages(self):
        return get_commit_messages(self)

    def commit_messages_since(self, since=None):
        return get_commit_messages(self, since=since)

    @property
    def can_view_commit(self):
        return self.git_username and self.git_password and self.git_repo

    @property
    def total_point(self):
        return round(Deliverable.objects.filter(~Q(status=DeliverableStatus.Rejected), task__project=self)\
                   .aggregate(total_point=Sum('estimated_hour')).get('total_point') or Decimal(0), 2)

    @property
    def percent_completed(self):
        total = self.total_point or Decimal(1)
        total_done = Deliverable.objects.filter(Q(status=DeliverableStatus.Done) | Q(status=DeliverableStatus.Delivered), task__project=self).aggregate(total_point=Sum('estimated_hour')).get('total_point') or Decimal(0)
        return round((total_done * Decimal(100)) / total, 2)


class ProjectCommitLog(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='commit_log')
    sha = models.CharField(max_length=256, unique=True)
    message = models.CharField(max_length=256)
    date = models.DateTimeField()
    author_name = models.CharField(max_length=128)
    author_email = models.CharField(max_length=128)
    url = models.URLField(max_length=128)
    html_url = models.URLField(max_length=128)


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    role = models.IntegerField(choices=ProjectMemberRole.choices, default=ProjectMemberRole.Developer)


class Release(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(default='', null=True, blank=True)
    version = models.CharField(max_length=100, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    release_date = models.DateField(default=None)
    delivery_date = models.DateField(default=None, null=True, blank=True)
    release_log = models.TextField(default=None, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name='created_releases')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name='approved_releases')
    comment = models.TextField(default='', null=True, blank=True)

    def __str__(self):
        return self.name


class UserStory(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=None)
    release = models.ForeignKey(Release, on_delete=models.CASCADE, default=None)
    summary = models.TextField(default='', verbose_name='Title')
    details = models.TextField(default='', null=True, blank=True)
    code = models.CharField(max_length=100, default='', null=True, blank=True)
    start_date = models.DateField(default=None, null=True, blank=True)
    end_date = models.DateField(default=None, null=True, blank=True)
    description = models.TextField(default='', null=True, blank=True)
    analysed_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name='analysed_user_stories')
    approved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name='approved_user_stories')
    status = models.IntegerField(choices=UserStoryStatus.choices, default=UserStoryStatus.Pending, null=True, blank=True)
    comment = models.TextField(default='', null=True, blank=True)

    def __str__(self):
        return self.summary

    class Meta:
        permissions = (
            ("update_user_story_status", "Can Update Status of User Story"),
        )


class Issue(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(default='', blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, default=None, null=True)
    user_story = models.ForeignKey(UserStory, on_delete=models.SET_NULL, default=None, null=True, blank=True)
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

    class Meta:
        permissions = (
            ("update_sprint_status", "Can Update Status of Sprint"),
            ("sprint_status_report", "Can See Sprint Status Report"),
            ("sprint_status_report_download", "Can Download Sprint Status Report"),
        )

    @property
    def is_current(self):
        today = datetime.datetime.today().date()
        return self.start_date <= today and self.end_date >= today

    @property
    def total_point(self):
        return round(Deliverable.objects.filter(~Q(status=DeliverableStatus.Rejected), sprint=self).aggregate(
            total_point=Sum('estimated_hour')).get('total_point') or Decimal(0))

    @property
    def percent_completed(self):
        total = self.total_point  or Decimal(1)
        total_done = Deliverable.objects.filter(
            Q(status=DeliverableStatus.Done) | Q(status=DeliverableStatus.Delivered), sprint=self).aggregate(
            total_point=Sum('estimated_hour')).get('total_point') or Decimal(0)
        return round((total_done * Decimal(100)) / total, 2)


class Task(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    release = models.ForeignKey(Release, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    user_story = models.ForeignKey(UserStory, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    category = models.IntegerField(choices=Category.choices, default=Category.Analysis, null=True, blank=True)
    responsible = models.ForeignKey(Employee, on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name='responsible_tasks')
    assignee = models.ForeignKey(Employee, on_delete=models.SET_NULL, default=None, null=True, related_name='assigned_tasks')
    estimation = models.DecimalField(default=0.0, decimal_places=2, max_digits=15)
    start_date = models.DateField(default=None)
    end_date = models.DateField(default=None, null=True, blank=True)
    priority = models.IntegerField(choices=Priority.choices, default=Priority.High, null=True)
    assigned_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name='assigned_by_tasks')
    assign_date = models.DateField(default=None, null=True, blank=True)
    approved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name='approved_by_tasks')
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
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, default=None, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(default='', null=True, blank=True)
    sprint = models.ForeignKey(Sprint, on_delete=models.SET_NULL, default=None, null=True)
    estimated_hour = models.DecimalField(verbose_name='Point', default=0.0, decimal_places=2, max_digits=15, null=True, blank=True)
    actual_hour = models.DecimalField(verbose_name='Actual Point', default=0.0, decimal_places=2, max_digits=15, null=True, blank=True)
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
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    release = models.ForeignKey(Release, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    user_story = models.ForeignKey(UserStory, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    issue = models.ForeignKey(Issue, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    sprint = models.ForeignKey(Sprint, on_delete=models.SET_NULL, default=None, null=True)
    deliverable = models.ForeignKey(Deliverable, on_delete=models.SET_NULL, default=None, null=True)
    entry_date = models.DateField(default=None, null=True, blank=True)
    estimated_hour = models.DecimalField(verbose_name='Point', default=0.0, decimal_places=2, max_digits=15, null=True, blank=True)
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

