from django.contrib import admin
from .models import ProjectType, Project, Release, UserStory

admin.site.register(ProjectType)
admin.site.register(Project)
admin.site.register(Release)
admin.site.register(UserStory)
