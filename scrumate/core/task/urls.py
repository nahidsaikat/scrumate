from django.urls import path
from scrumate.core.task import views


urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('add/', views.task_add, name='task_add'),
    path('<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('<int:pk>/update_status/', views.update_task_status, name='update_task_status'),
]