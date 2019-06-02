from django.urls import path
from scrumate.core.member import views


urlpatterns = [
    path('', views.project_member_list, name='project_member_list'),
    path('add/', views.project_member_add, name='project_member_add'),
    path('<int:pk>/edit/', views.project_member_edit, name='project_member_edit'),
    path('<int:pk>/delete/', views.project_member_delete, name='project_member_delete'),
]
