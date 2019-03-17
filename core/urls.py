from django.urls import path
from . import views


urlpatterns = [
    path('project/', views.project_list, name='project_list'),
    path('project/add/', views.project_add, name='project_add'),
    path('release/', views.release_list, name='release_list'),
    path('release/add/', views.release_add, name='release_add'),
    path('user_story/', views.user_story_list, name='user_story_list'),
    path('user_story/add/', views.user_story_add, name='user_story_add'),
    path('sprint/', views.user_story_list, name='sprint_list'),
    path('sprint/add/', views.user_story_add, name='sprint_add'),
]
