from django.db import models


class Post(models.Model):
    title        = models.CharField(max_length=300)
    content      = models.TextField()
    cover_image  = models.ImageField(upload_to='posts/', blank=True, null=True)
    is_published = models.BooleanField(default=True)
    is_featured  = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class PostMedia(models.Model):
    MEDIA_TYPE = [('image', 'Image'), ('video', 'Video')]
    post       = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media_files')
    file       = models.FileField(upload_to='posts/media/')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE, default='image')
    order      = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.post.title} — {self.media_type} #{self.order}"
