from django.contrib import admin
from .models import FAQItem, ChatSession, ChatMessage

@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = ['question', 'is_active', 'order']
    list_editable = ['is_active', 'order']

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'created_at', 'updated_at']
    readonly_fields = ['session_key', 'created_at', 'updated_at']

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'role', 'content', 'created_at']
    list_filter = ['role']
