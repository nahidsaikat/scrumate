import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum, Q

from scrumate.core.deliverable.choices import DeliverableStatus
from scrumate.core.project.models import Project
from scrumate.core.sprint.choices import SprintStatus
from scrumate.core.task.choices import TaskStatus, Category
from scrumate.general.choices import Priority
from scrumate.people.models import Employee, Department

User = get_user_model()


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

