from django.urls import path
from scrumate.core.issue import views


urlpatterns = [
    path('', views.issue_list, name='issue_list'),
    path('add/', views.issue_add, name='issue_add'),
    path('<int:pk>/edit/', views.issue_edit, name='issue_edit'),
    path('<int:pk>/update_status/', views.update_issue_status, name='update_issue_status'),
    path('<int:pk>/history/', views.IssueHistoryList.as_view(), name='issue_history'),
]
