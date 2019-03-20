from django.urls import path
from . import views


urlpatterns = [
    # Accounts
    path('profile/', views.profile, name='profile'),
    path('change_password/', views.change_password, name='change_password'),

    # Main functionalities
    path('project/', views.project_list, name='project_list'),
    path('project/add/', views.project_add, name='project_add'),
    path('release/', views.release_list, name='release_list'),
    path('release/add/', views.release_add, name='release_add'),
    path('user_story/', views.user_story_list, name='user_story_list'),
    path('user_story/add/', views.user_story_add, name='user_story_add'),
    path('sprint/', views.sprint_list, name='sprint_list'),
    path('sprint/add/', views.sprint_add, name='sprint_add'),
    path('task/', views.task_list, name='task_list'),
    path('task/add/', views.task_add, name='task_add'),
    path('deliverable/', views.deliverable_list, name='deliverable_list'),
    path('deliverable/add/', views.deliverable_add, name='deliverable_add'),
    path('issue/', views.issue_list, name='issue_list'),
    path('issue/add/', views.issue_add, name='issue_add'),
    path('daily_scrum/', views.daily_scrum_list, name='daily_scrum_list'),
    path('daily_scrum/add/', views.daily_scrum_add, name='daily_scrum_add'),

    # Settings
    path('department/', views.department_list, name='department_list'),
    path('department/add/', views.department_add, name='department_add'),
    path('designation/', views.designation_list, name='designation_list'),
    path('designation/add/', views.designation_add, name='designation_add'),
    path('employee/', views.employee_list, name='employee_list'),
    path('employee/add/', views.employee_add, name='employee_add'),
    path('client/', views.client_list, name='client_list'),
    path('client/add/', views.client_add, name='client_add'),
]
