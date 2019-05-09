from django.urls import path
from . import views
from . import api



urlpatterns = [
    # Accounts
    path('profile/', views.profile, name='profile'),
    path('change_password/', views.change_password, name='change_password'),

    # Main functionalities
    path('project/', views.project_list, name='project_list'),
    path('project/add/', views.project_add, name='project_add'),
    path('project/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('project/<int:pk>/update_status/', views.update_project_status, name='update_project_status'),
    path('project/<int:pk>/view_commit_logs/', views.view_commit_logs, name='view_commit_logs'),

    path('release/', views.release_list, name='release_list'),
    path('release/add/', views.release_add, name='release_add'),
    path('release/<int:pk>/edit/', views.release_edit, name='release_edit'),

    path('user_story/', views.user_story_list, name='user_story_list'),
    path('user_story/add/', views.user_story_add, name='user_story_add'),
    path('user_story/<int:pk>/edit/', views.user_story_edit, name='user_story_edit'),
    path('user_story/<int:pk>/update_status/', views.update_user_story_status, name='update_user_story_status'),

    path('sprint/', views.sprint_list, name='sprint_list'),
    path('sprint/add/', views.sprint_add, name='sprint_add'),
    path('sprint/<int:pk>/edit/', views.sprint_edit, name='sprint_edit'),
    path('sprint/<int:pk>/update_status/', views.update_sprint_status, name='update_sprint_status'),
    path('sprint/status_report/', views.status_report, name='status_report'),
    path('sprint/<int:pk>/download/', views.status_report_download, name='status_report_download'),

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

    path('daily_scrum/', views.daily_scrum_list, name='daily_scrum_list'),
    path('daily_scrum/add/', views.daily_scrum_add, name='daily_scrum_add'),
    path('daily_scrum/<int:pk>/edit/', views.daily_scrum_edit, name='daily_scrum_edit'),
    path('daily_scrum/<int:pk>/set_actual_hour/', views.set_actual_hour, name='set_actual_hour'),
    path('daily_scrum/<int:pk>/update_actual_hour/', views.update_actual_hour, name='update_actual_hour'),

    # Settings
    path('department/', views.department_list, name='department_list'),
    path('department/add/', views.department_add, name='department_add'),
    path('department/<int:pk>/edit/', views.department_edit, name='department_edit'),

    path('designation/', views.designation_list, name='designation_list'),
    path('designation/add/', views.designation_add, name='designation_add'),
    path('designation/<int:pk>/edit/', views.designation_edit, name='designation_edit'),

    path('employee/', views.employee_list, name='employee_list'),
    path('employee/add/', views.employee_add, name='employee_add'),
    path('employee/<int:pk>/edit/', views.employee_edit, name='employee_edit'),

    path('client/', views.client_list, name='client_list'),
    path('client/add/', views.client_add, name='client_add'),
    path('client/<int:pk>/edit/', views.client_edit, name='client_edit'),

    # API
    path('task/<int:pk>/task_info/', api.task_info, name='task_info'),
    path('deliverable/<int:pk>/deliverable_info/', api.deliverable_info, name='deliverable_info'),
]
