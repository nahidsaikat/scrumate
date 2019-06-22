import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum, Q
from simple_history.models import HistoricalRecords

from scrumate.core.deliverable.choices import DeliverableStatus
from scrumate.core.project.choices import ProjectType, ProjectStatus
from scrumate.general.source_control import get_commit_messages
from scrumate.people.models import Client

User = get_user_model()


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

    history = HistoricalRecords()

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
            ("project_history", "Can See Project History"),
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
        from scrumate.core.deliverable.models import Deliverable
        return round(Deliverable.objects.filter(~Q(status=DeliverableStatus.Rejected), task__project=self)\
                   .aggregate(total_point=Sum('estimated_hour')).get('total_point') or Decimal(0), 2)

    @property
    def percent_completed(self):
        from scrumate.core.deliverable.models import Deliverable
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

    history = HistoricalRecords()


class OverTime(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, default=None, null=True)
    work_date = models.DateField(default=None)
    description = models.TextField(default='')
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, related_name='assignee_over_times')
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, related_name='assigned_by_over_times')
    comment = models.TextField(default='')
    status = models.IntegerField(choices=DeliverableStatus.choices, default=DeliverableStatus.Pending)

    history = HistoricalRecords()
