from django.db import models
from simple_history.models import HistoricalRecords

from scrumate.core.issue.models import Issue
from scrumate.core.project.models import Project
from scrumate.core.release.models import Release
from scrumate.core.task.choices import Category, TaskStatus
from scrumate.core.user_story.models import UserStory
from scrumate.general.choices import Priority
from scrumate.people.models import Employee


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

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ("update_task_status", "Can Update Status of Task"),
        )
