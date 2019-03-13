from django.urls import path
from . import views


urlpatterns = [
    path('project/', views.project_list, name='project_list'),
    path('project/add/', views.project_add, name='project_add'),
]
