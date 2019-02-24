from django.contrib import admin
from .models import ProjectType, Project, Release, UserStory, Division, Department, Designation, Dashboard, Portlet, \
    DashboardPortlet, Priority, Label, Issue, Sprint, Task

admin.site.register(ProjectType)
admin.site.register(Project)
admin.site.register(Release)
admin.site.register(UserStory)
admin.site.register(Division)
admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Dashboard)
admin.site.register(Portlet)
admin.site.register(DashboardPortlet)
admin.site.register(Priority)
admin.site.register(Label)
admin.site.register(Issue)
admin.site.register(Sprint)
admin.site.register(Task)
