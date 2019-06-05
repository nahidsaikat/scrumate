from django.contrib import admin

from scrumate.core.deliverable.models import Deliverable
from scrumate.core.project.models import ProjectCommitLog, Project
from scrumate.core.release.models import Release
from scrumate.core.sprint.models import Sprint
from scrumate.core.task.models import Task
from scrumate.core.user_story.models import UserStory

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
