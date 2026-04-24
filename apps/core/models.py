from django.db import models

class Inquiry(models.Model):
    STATUS = [('new', 'New'), ('read', 'Read'), ('replied', 'Replied')]
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Inquiries'

    def __str__(self):
        return f"{self.name} — {self.subject}"

class SiteSettings(models.Model):
    venue_name = models.CharField(max_length=100, default='Kakahoyan')
    tagline = models.CharField(max_length=300, blank=True)
    phone = models.CharField(max_length=20, default='0920 611 2718')
    email = models.EmailField(blank=True)
    address = models.TextField(default='Purok 2, Brgy. Caranoche, Sta. Catalina, Negros Oriental, 6220')
    facebook_url = models.URLField(blank=True)
    google_maps_embed = models.TextField(blank=True, help_text='Full Google Maps embed iframe code')
    max_indoor_capacity = models.PositiveIntegerField(default=250)
    max_outdoor_capacity = models.PositiveIntegerField(default=500)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return 'Site Settings'
