import datetime
from decimal import Decimal

from django.db import models
from django.db.models import Sum

from scrumate.core.deliverable.choices import DeliverableStatus
from scrumate.core.project.models import Project
from scrumate.core.sprint.choices import SprintStatus
from scrumate.people.models import Department


class Sprint(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(default='', null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    start_date = models.DateField(default=None, null=True, blank=True)
    end_date = models.DateField(default=None, null=True, blank=True)
    day_wise_label = models.TextField(default='', null=True, blank=True)
    status = models.IntegerField(choices=SprintStatus.choices, default=1, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, default=None, null=True)

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
        from scrumate.core.deliverable.models import Deliverable
        return round(Deliverable.objects.filter(~Q(status=DeliverableStatus.Rejected), sprint=self).aggregate(
            total_point=Sum('estimated_hour')).get('total_point') or Decimal(0))

    @property
    def percent_completed(self):
        from scrumate.core.deliverable.models import Deliverable
        total = self.total_point  or Decimal(1)
        total_done = Deliverable.objects.filter(
            Q(status=DeliverableStatus.Done) | Q(status=DeliverableStatus.Delivered), sprint=self).aggregate(
            total_point=Sum('estimated_hour')).get('total_point') or Decimal(0)
        return round((total_done * Decimal(100)) / total, 2)
