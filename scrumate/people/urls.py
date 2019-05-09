from django.urls import path
from scrumate.people import views


urlpatterns = [
    # Accounts
    path('profile/', views.profile, name='profile'),
    path('change_password/', views.change_password, name='change_password'),

    # Settings
    path('department/', views.department_list, name='department_list'),
    path('department/add/', views.department_add, name='department_add'),
    path('department/<int:pk>/edit/', views.department_edit, name='department_edit'),

    path('designation/', views.designation_list, name='designation_list'),
    path('designation/add/', views.designation_add, name='designation_add'),
    path('designation/<int:pk>/edit/', views.designation_edit, name='designation_edit'),

    path('employee/', views.employee_list, name='employee_list'),
    path('employee/add/', views.employee_add, name='employee_add'),
    path('employee/<int:pk>/edit/', views.employee_edit, name='employee_edit'),

    path('client/', views.client_list, name='client_list'),
    path('client/add/', views.client_add, name='client_add'),
    path('client/<int:pk>/edit/', views.client_edit, name='client_edit'),
]
