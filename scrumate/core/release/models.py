from django.db import models
from django.contrib.auth import get_user_model
from simple_history.models import HistoricalRecords

from scrumate.core.project.models import Project

User = get_user_model()


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

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ("release_history", "Can See Release History"),
        )
