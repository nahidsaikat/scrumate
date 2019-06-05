from django.db import models

from scrumate.core.deliverable.choices import DeliverableStatus
from scrumate.core.project.models import Project
from scrumate.core.user_story.models import UserStory
from scrumate.people.models import Employee


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
