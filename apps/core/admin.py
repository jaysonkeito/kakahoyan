from django.contrib import admin
from django.utils.html import format_html
from .models import Inquiry, SiteSettings, Service, Facility, FacilityImage, ManagementTeam


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {'fields': ('venue_name', 'tagline', 'hero_description', 'hours')}),
        ('Contact',    {'fields': ('phone', 'email', 'address', 'facebook_url')}),
        ('Capacity',   {'fields': ('max_indoor_capacity', 'max_outdoor_capacity')}),
        ('Maps',       {'fields': ('google_maps_embed',)}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display  = ('name', 'email', 'subject', 'status', 'created_at')
    list_filter   = ('status',)
    search_fields = ('name', 'email', 'subject')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display  = ('name', 'icon', 'is_active', 'order')
    list_editable = ('is_active', 'order')


class FacilityImageInline(admin.TabularInline):
    model  = FacilityImage
    extra  = 1
    max_num = 5
    fields = ('image', 'caption', 'order')


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display  = ('name', 'is_featured', 'order')
    list_editable = ('is_featured', 'order')
    inlines       = [FacilityImageInline]


@admin.register(ManagementTeam)
class ManagementTeamAdmin(admin.ModelAdmin):
    list_display  = ('name', 'role', 'is_active', 'order')
    list_editable = ('is_active', 'order')
