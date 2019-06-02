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

    path('task/', views.task_list, name='task_list'),
    path('task/add/', views.task_add, name='task_add'),
    path('task/<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('task/<int:pk>/update_status/', views.update_task_status, name='update_task_status'),

    path('deliverable/', views.deliverable_list, name='deliverable_list'),
    path('deliverable/add/', views.deliverable_add, name='deliverable_add'),
    path('deliverable/<int:pk>/edit/', views.deliverable_edit, name='deliverable_edit'),
    path('deliverable/<int:pk>/update_status/', views.update_deliverable_status, name='update_deliverable_status'),

    path('issue/', views.issue_list, name='issue_list'),
    path('issue/add/', views.issue_add, name='issue_add'),
    path('issue/<int:pk>/edit/', views.issue_edit, name='issue_edit'),
    path('issue/<int:pk>/update_status/', views.update_issue_status, name='update_issue_status'),

    path('sprint/', include('scrumate.core.sprint.urls'), name='sprint'),
    path('member/', include('scrumate.core.project.member.urls'), name='member'),
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
