from django.db import models

class MediaCategory(models.Model):
    name  = models.CharField(max_length=100)
    slug  = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Media Categories'

    def __str__(self):
        return self.name


class MediaItem(models.Model):
    MEDIA_TYPES = [('photo', 'Photo'), ('video', 'Video')]

    category    = models.ForeignKey(MediaCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='items')
    title       = models.CharField(max_length=200, blank=True)
    media_type  = models.CharField(max_length=10, choices=MEDIA_TYPES, default='photo')
    file        = models.FileField(upload_to='gallery/')
    thumbnail   = models.ImageField(upload_to='gallery/thumbs/', blank=True, null=True)
    description = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)
    order       = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-uploaded_at']

    def __str__(self):
        return self.title or f"{self.media_type} #{self.pk}"
