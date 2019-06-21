from django.db import models
from simple_history.models import HistoricalRecords

from scrumate.core.deliverable.models import Deliverable
from scrumate.core.issue.models import Issue
from scrumate.core.project.models import Project
from scrumate.core.release.models import Release
from scrumate.core.sprint.models import Sprint
from scrumate.core.task.models import Task
from scrumate.core.user_story.models import UserStory
from scrumate.people.models import Employee


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

    history = HistoricalRecords()

    def __str__(self):
        return self.project.name + ' ' + self.task.name

    class Meta:
        permissions = (
            ("set_actual_hour", "Can Set Actual Hour of Daily Scrum"),
            ("update_actual_hour", "Can Update Actual Hour of Daily Scrum"),
        )
