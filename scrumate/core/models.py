from django.contrib.auth import get_user_model
from django.db import models

from scrumate.core.deliverable.choices import DeliverableStatus
from scrumate.core.project.models import Project
from scrumate.core.task.choices import TaskStatus, Category
from scrumate.general.choices import Priority
from scrumate.people.models import Employee

User = get_user_model()


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

