from django.urls import path
from . import views
urlpatterns = [
    path('message/', views.chat_message, name='chat_message'),
    path('faqs/', views.get_faqs, name='get_faqs'),
]
