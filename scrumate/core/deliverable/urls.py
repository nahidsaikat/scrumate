from django.urls import path
from scrumate.core.deliverable import views


urlpatterns = [
    path('', views.deliverable_list, name='deliverable_list'),
    path('add/', views.deliverable_add, name='deliverable_add'),
    path('<int:pk>/edit/', views.deliverable_edit, name='deliverable_edit'),
    path('<int:pk>/update_status/', views.update_deliverable_status, name='update_deliverable_status'),
    path('<int:pk>/history/', views.DeliverableHistoryList.as_view(), name='deliverable_history'),
]
