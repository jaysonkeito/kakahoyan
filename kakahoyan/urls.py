from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('gallery/', include('apps.gallery.urls')),
    path('appointments/', include('apps.appointments.urls')),
    path('chatbot/', include('apps.chatbot.urls')),
    path('posts/', include('apps.posts.urls')),
    path('admin-panel/', include('apps.admin_panel.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
