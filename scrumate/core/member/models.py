from django.db import models

from scrumate.core.member.choices import ProjectMemberRole
from scrumate.core.project.models import Project
from scrumate.people.models import Employee


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    role = models.IntegerField(choices=ProjectMemberRole.choices, default=ProjectMemberRole.Developer)
