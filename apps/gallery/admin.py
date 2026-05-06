from django.contrib import admin
from .models import MediaItem, MediaCategory

@admin.register(MediaCategory)
class MediaCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'media_type', 'category', 'is_featured', 'order', 'uploaded_at']
    list_filter = ['media_type', 'category', 'is_featured']
    list_editable = ['is_featured', 'order']
    search_fields = ['title', 'description']
