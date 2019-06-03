from django.urls import path
from scrumate.core.daily_scrum import views


urlpatterns = [
    path('', views.daily_scrum_entry, name='daily_scrum'),
    path('<int:deliverable_id>/set_actual_hour/', views.set_actual_hour, name='set_actual_hour'),
    path('<int:deliverable_id>/update_actual_hour/', views.update_actual_hour, name='update_actual_hour'),
    path('<int:deliverable_id>/assign_dev/', views.assign_dev, name='assign_dev'),
]
