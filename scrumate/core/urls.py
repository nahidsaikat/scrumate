from django.urls import path, include
from scrumate.core import views
from scrumate.core import api

project_view_urlpatterns = [
    path('release/', include('scrumate.core.release.urls'), name='release'),
    path('user_story/', include('scrumate.core.user_story.urls'), name='user_story'),
    path('task/', include('scrumate.core.task.urls'), name='task'),
    path('deliverable/', include('scrumate.core.deliverable.urls'), name='deliverable'),
    path('issue/', include('scrumate.core.issue.urls'), name='issue'),
    path('sprint/', include('scrumate.core.sprint.urls'), name='sprint'),
    path('member/', include('scrumate.core.member.urls'), name='member'),
]

urlpatterns = [
    # Main functionalities
    path('project/<int:project_id>/', include(project_view_urlpatterns), name='project_view'),
    path('project/', include('scrumate.core.project.urls'), name='project'),

    path('daily_scrum/', views.daily_scrum_entry, name='daily_scrum'),
    path('daily_scrum/<int:deliverable_id>/set_actual_hour/', views.set_actual_hour, name='set_actual_hour'),
    path('daily_scrum/<int:deliverable_id>/update_actual_hour/', views.update_actual_hour, name='update_actual_hour'),
    path('daily_scrum/<int:deliverable_id>/assign_dev/', views.assign_dev, name='assign_dev'),

    # API
    path('task/<int:pk>/task_info/', api.task_info, name='task_info'),
    path('deliverable/<int:pk>/deliverable_info/', api.deliverable_info, name='deliverable_info'),
]
