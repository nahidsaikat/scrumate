from django.urls import path
from scrumate.core.deliverable import views
from scrumate.core.deliverable import api


urlpatterns = [
    path('', views.deliverable_list, name='deliverable_list'),
    path('add/', views.deliverable_add, name='deliverable_add'),
    path('<int:pk>/', views.DeliverableDetailView.as_view(), name='deliverable_view'),
    path('<int:pk>/edit/', views.deliverable_edit, name='deliverable_edit'),
    path('<int:pk>/update_status/', views.update_deliverable_status, name='update_deliverable_status'),
    path('<int:pk>/history/', views.DeliverableHistoryList.as_view(), name='deliverable_history'),

    # API
    path('<int:pk>/deliverable_info/', api.deliverable_info, name='deliverable_info'),
]
