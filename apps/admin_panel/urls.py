from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'admin_panel'
urlpatterns = [
    path('login/',   auth_views.LoginView.as_view(template_name='admin_panel/login.html'), name='login'),
    path('logout/',  auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Media
    path('media/',                    views.media_list_view,   name='media_list'),
    path('media/upload/',             views.media_upload_view, name='media_upload'),
    path('media/<int:pk>/delete/',    views.media_delete_view, name='media_delete'),

    # Posts
    path('posts/',                    views.posts_list_view,   name='posts_list'),
    path('posts/create/',             views.post_create_view,  name='post_create'),
    path('posts/<int:pk>/edit/',      views.post_edit_view,    name='post_edit'),
    path('posts/<int:pk>/delete/',    views.post_delete_view,  name='post_delete'),

    # Appointments
    path('appointments/',             views.appointments_list_view,   name='appointments_list'),
    path('appointments/<int:pk>/',    views.appointment_detail_view,  name='appointment_detail'),

    # Chatbot logs
    path('inquiries/',                views.inquiries_list_view, name='inquiries_list'),

    # Site settings
    path('settings/',                 views.site_settings_view, name='site_settings'),

    # Services
    path('services/',                 views.services_list_view,   name='services_list'),
    path('services/create/',          views.service_create_view,  name='service_create'),
    path('services/<int:pk>/edit/',   views.service_edit_view,    name='service_edit'),
    path('services/<int:pk>/delete/', views.service_delete_view,  name='service_delete'),

    # Facilities
    path('facilities/',                 views.facilities_list_view,   name='facilities_list'),
    path('facilities/create/',          views.facility_create_view,   name='facility_create'),
    path('facilities/<int:pk>/edit/',   views.facility_edit_view,     name='facility_edit'),
    path('facilities/<int:pk>/delete/', views.facility_delete_view,   name='facility_delete'),

    # Management Team
    path('team/',                     views.team_list_view,   name='team_list'),
    path('team/create/',              views.team_create_view, name='team_create'),
    path('team/<int:pk>/edit/',       views.team_edit_view,   name='team_edit'),
    path('team/<int:pk>/delete/',     views.team_delete_view, name='team_delete'),
]
