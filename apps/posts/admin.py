from django.contrib import admin
from .models import Post, PostMedia


class PostMediaInline(admin.TabularInline):
    model  = PostMedia
    extra  = 1
    fields = ('file', 'media_type', 'order')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display  = ('title', 'is_published', 'is_featured', 'created_at')
    list_editable = ('is_published', 'is_featured')
    inlines       = [PostMediaInline]
