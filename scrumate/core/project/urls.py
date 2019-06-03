from django.urls import path
from scrumate.core.project import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('add/', views.project_add, name='project_add'),
    path('<int:project_id>/edit/', views.project_edit, name='project_edit'),
    path('<int:project_id>/update_status/', views.update_project_status, name='update_project_status'),
    path('<int:project_id>/view_commit_logs/', views.view_commit_logs, name='view_commit_logs'),
    path('<int:project_id>/sync_commit/', views.sync_commit, name='sync_commit'),
]
