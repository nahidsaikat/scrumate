from django.urls import path
from scrumate.core.release import views


urlpatterns = [
    path('', views.release_list, name='release_list'),
    path('add/', views.release_add, name='release_add'),
    path('<int:pk>/edit/', views.release_edit, name='release_edit'),
]
