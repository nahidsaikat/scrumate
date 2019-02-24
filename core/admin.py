from django.contrib import admin
from .models import ProjectType, Project, Release, UserStory, Division, Department, Designation

admin.site.register(ProjectType)
admin.site.register(Project)
admin.site.register(Release)
admin.site.register(UserStory)
admin.site.register(Division)
admin.site.register(Department)
admin.site.register(Designation)
