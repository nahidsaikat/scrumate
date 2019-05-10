from django.urls import path

from scrumate.general import views


urlpatterns = [
    path('settings/', views.settings, name='settings'),
]
