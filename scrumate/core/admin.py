from django.contrib import admin

from .models import Project, Release, UserStory, Sprint, Task, Deliverable
from scrumate.core.project.models import ProjectCommitLog

admin.site.register(Project)
admin.site.register(ProjectCommitLog)
admin.site.register(Release)
admin.site.register(UserStory)
# admin.site.register(Division)
# admin.site.register(Dashboard)
# admin.site.register(Portlet)
# admin.site.register(DashboardPortlet)
# admin.site.register(Priority)
# admin.site.register(Label)
# admin.site.register(Issue)
admin.site.register(Sprint)
admin.site.register(Task)
admin.site.register(Deliverable)
# admin.site.register(DailyScrum)
# admin.site.register(OverTime)
# admin.site.register(Party)
