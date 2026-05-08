from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('student/', views.student_dashboard, name='student_dashboard'),
    path('agency/', views.agency_dashboard, name='agency_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),

    path('add-opportunity/', views.add_opportunity, name='add_opportunity'),
    path('view-volunteers/', views.view_volunteers, name='view_volunteers'),

    path('manage-users/', views.manage_users, name='manage_users'),

    path(
        'toggle-user/<int:pk>/',
        views.toggle_user_status,
        name='toggle_user_status'
    ),

    path(
        'delete-user/<int:pk>/',
        views.delete_user,
        name='delete_user'
    ),

    path('approve-hours/', views.approve_hours, name='approve_hours'),

    path(
        'complete-application/<int:pk>/',
        views.complete_application,
        name='complete_application'
    ),

    path(
        'accept-application/<int:pk>/',
        views.accept_application,
        name='accept_application'
    ),

    path(
        'reject-application/<int:pk>/',
        views.reject_application,
        name='reject_application'
    ),

    path(
        'confirm-participation/<int:pk>/',
        views.confirm_participation,
        name='confirm_participation'
    ),
]