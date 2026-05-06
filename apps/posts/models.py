from django.db import models

class Post(models.Model):
    title        = models.CharField(max_length=300)
    content      = models.TextField()
    image        = models.ImageField(upload_to='posts/', blank=True, null=True)
    is_published = models.BooleanField(default=True)
    is_featured  = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
