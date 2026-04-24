from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'admin_panel'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='admin_panel/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('media/', views.media_list_view, name='media_list'),
    path('media/upload/', views.media_upload_view, name='media_upload'),
    path('media/<int:pk>/delete/', views.media_delete_view, name='media_delete'),
    path('posts/', views.posts_list_view, name='posts_list'),
    path('posts/create/', views.post_create_view, name='post_create'),
    path('posts/<int:pk>/edit/', views.post_edit_view, name='post_edit'),
    path('posts/<int:pk>/delete/', views.post_delete_view, name='post_delete'),
    path('appointments/', views.appointments_list_view, name='appointments_list'),
    path('appointments/<int:pk>/', views.appointment_detail_view, name='appointment_detail'),
    path('inquiries/', views.inquiries_list_view, name='inquiries_list'),
]
