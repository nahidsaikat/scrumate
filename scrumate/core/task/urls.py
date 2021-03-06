from django.urls import path
from scrumate.core.task import views
from scrumate.core.task import api


urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('add/', views.task_add, name='task_add'),
    path('<int:pk>/', views.TaskDetailView.as_view(), name='task_view'),
    path('<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('<int:pk>/update_status/', views.update_task_status, name='update_task_status'),
    path('<int:pk>/history/', views.TaskHistoryList.as_view(), name='task_history'),

    #API
    path('<int:pk>/task_info/', api.task_info, name='task_info'),
]
