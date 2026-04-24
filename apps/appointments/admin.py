from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'event_type', 'discussion_date', 'discussion_time', 'discussion_type', 'status', 'created_at']
    list_filter = ['status', 'event_type', 'discussion_type']
    list_editable = ['status']
    search_fields = ['client_name', 'client_email', 'client_phone']
    readonly_fields = ['created_at', 'updated_at']
