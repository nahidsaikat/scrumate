from django.urls import path

from scrumate.general import views


urlpatterns = [
    path('settings/', views.settings, name='settings'),
    path('reports/', views.reports, name='reports'),
    path('project/', views.project, name='project'),
    path('project/<int:project_id>/', views.project_dashboard, name='project_dashboard'),
]
