from django.urls import path
from scrumate.core.report import views


urlpatterns = [
    path('sprint/sprint_status_report/', views.sprint_status_report, name='sprint_status_report'),
    path('sprint/<int:pk>/sprint_status/download/', views.sprint_status_report_download, name='sprint_status_report_download'),
    path('project/project_status_report/', views.project_status_report, name='project_status_report'),
    path('project/<int:project_id>/project_status/download/', views.project_status_report_download, name='project_status_report_download'),
]