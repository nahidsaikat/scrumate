from django.urls import path
from scrumate.core.sprint import views


urlpatterns = [
    path('', views.sprint_list, name='sprint_list'),
    path('add/', views.sprint_add, name='sprint_add'),
    path('<int:pk>/edit/', views.sprint_edit, name='sprint_edit'),
    path('<int:pk>/', views.sprint_view, name='sprint_view'),
    path('<int:pk>/update_status/', views.update_sprint_status, name='update_sprint_status'),
    path('sprint_status_report/', views.sprint_status_report, name='sprint_status_report'),
    path('<int:pk>/sprint_status/download/', views.sprint_status_report_download, name='sprint_status_report_download'),
]
