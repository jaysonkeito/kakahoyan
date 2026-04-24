from django.contrib import admin
from .models import Inquiry, SiteSettings

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'created_at']
    list_filter = ['status']
    list_editable = ['status']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at']

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()
