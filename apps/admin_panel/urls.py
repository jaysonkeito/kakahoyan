from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'admin_panel'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='admin_panel/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Analytics
    path('analytics/', views.analytics_view, name='analytics'),

    # Media
    path('media/', views.media_list_view, name='media_list'),
    path('media/upload/', views.media_upload_view, name='media_upload'),
    path('media/<int:pk>/delete/', views.media_delete_view, name='media_delete'),

    # Posts
    path('posts/', views.posts_list_view, name='posts_list'),
    path('posts/create/', views.post_create_view, name='post_create'),
    path('posts/<int:pk>/edit/', views.post_edit_view, name='post_edit'),
    path('posts/<int:pk>/delete/', views.post_delete_view, name='post_delete'),

    # Services
    path('services/', views.services_list_view, name='services_list'),
    path('services/create/', views.service_create_view, name='service_create'),
    path('services/<int:pk>/edit/', views.service_edit_view, name='service_edit'),
    path('services/<int:pk>/delete/', views.service_delete_view, name='service_delete'),

    # Amenities
    path('amenities/', views.amenities_list_view, name='amenities_list'),
    path('amenities/create/', views.amenity_create_view, name='amenity_create'),
    path('amenities/<int:pk>/edit/', views.amenity_edit_view, name='amenity_edit'),
    path('amenities/<int:pk>/delete/', views.amenity_delete_view, name='amenity_delete'),

    # Team
    path('team/', views.team_list_view, name='team_list'),
    path('team/create/', views.team_create_view, name='team_create'),
    path('team/<int:pk>/edit/', views.team_edit_view, name='team_edit'),
    path('team/<int:pk>/delete/', views.team_delete_view, name='team_delete'),

    # Appointments
    path('appointments/', views.appointments_list_view, name='appointments_list'),
    path('appointments/<int:pk>/', views.appointment_detail_view, name='appointment_detail'),

    # Event Records
    path('events/', views.events_list_view, name='events_list'),
    path('events/create/<int:appt_pk>/', views.event_create_view, name='event_create'),
    path('events/<int:pk>/', views.event_detail_view, name='event_detail'),

    # Inquiries / Chatbot logs
    path('inquiries/', views.inquiries_list_view, name='inquiries_list'),

    # Site Settings
    path('settings/', views.site_settings_view, name='site_settings'),
]
