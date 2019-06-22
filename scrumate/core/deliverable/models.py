from django.db import models
from simple_history.models import HistoricalRecords

from scrumate.core.deliverable.choices import DeliverableStatus
from scrumate.core.task.models import Task
from scrumate.core.project.models import Project
from scrumate.core.sprint.models import Sprint
from scrumate.general.choices import Priority
from scrumate.people.models import Employee


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

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ("update_deliverable_status", "Can Update Status of Deliverable"),
            ("deliverable_history", "Can See Deliverable History"),
        )