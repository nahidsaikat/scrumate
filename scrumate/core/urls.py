from django.urls import path, include
from scrumate.core import views
from scrumate.core import api

project_view_urlpatterns = [
    path('release/', views.release_list, name='release_list'),
    path('release/add/', views.release_add, name='release_add'),
    path('release/<int:pk>/edit/', views.release_edit, name='release_edit'),

    path('user_story/', views.user_story_list, name='user_story_list'),
    path('user_story/add/', views.user_story_add, name='user_story_add'),
    path('user_story/<int:pk>/edit/', views.user_story_edit, name='user_story_edit'),
    path('user_story/<int:pk>/update_status/', views.update_user_story_status, name='update_user_story_status'),

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

    path('daily_scrum/', views.daily_scrum_list, name='daily_scrum_list'),
    path('daily_scrum/add/', views.daily_scrum_add, name='daily_scrum_add'),
    path('daily_scrum/<int:pk>/edit/', views.daily_scrum_edit, name='daily_scrum_edit'),
    path('daily_scrum/<int:pk>/set_actual_hour/', views.set_actual_hour, name='set_actual_hour'),
    path('daily_scrum/<int:pk>/update_actual_hour/', views.update_actual_hour, name='update_actual_hour'),

    # API
    path('task/<int:pk>/task_info/', api.task_info, name='task_info'),
    path('deliverable/<int:pk>/deliverable_info/', api.deliverable_info, name='deliverable_info'),
]
