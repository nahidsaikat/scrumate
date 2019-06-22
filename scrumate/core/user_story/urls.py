from django.urls import path
from scrumate.core.user_story import views


urlpatterns = [
    path('', views.user_story_list, name='user_story_list'),
    path('add/', views.user_story_add, name='user_story_add'),
    path('<int:pk>/edit/', views.user_story_edit, name='user_story_edit'),
    path('<int:pk>/update_status/', views.update_user_story_status, name='update_user_story_status'),
    path('<int:pk>/history/', views.UserStoryHistoryList.as_view(), name='user_story_history'),
]
