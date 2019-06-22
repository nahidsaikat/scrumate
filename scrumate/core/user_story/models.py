from django.db import models
from simple_history.models import HistoricalRecords

from scrumate.core.project.models import Project
from scrumate.core.release.models import Release
from scrumate.core.user_story.choices import UserStoryStatus
from scrumate.people.models import Employee


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

    history = HistoricalRecords()

    def __str__(self):
        return self.summary

    class Meta:
        permissions = (
            ("update_user_story_status", "Can Update Status of User Story"),
            ("user_story_history", "Can See User Story History"),
        )
