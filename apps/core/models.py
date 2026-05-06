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
    hero_description = models.TextField(blank=True)   # ← ADD THIS
    phone = models.CharField(max_length=20, default='0920 611 2718')
    email = models.EmailField(blank=True)
    hours = models.CharField(max_length=100, blank=True)  # ← ADD THIS
    address = models.TextField(default='Purok 2, Brgy. Caranoche, Sta. Catalina, Negros Oriental, 6220')
    facebook_url = models.URLField(blank=True)
    google_maps_embed = models.TextField(blank=True)
    max_indoor_capacity = models.PositiveIntegerField(default=250)
    max_outdoor_capacity = models.PositiveIntegerField(default=500)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return 'Site Settings'


class Service(models.Model):
    ICON_CHOICES = [
        ('bi-hearts', 'Weddings'),
        ('bi-balloon', 'Birthdays'),
        ('bi-people', 'Reunions'),
        ('bi-mortarboard', 'Graduation'),
        ('bi-briefcase', 'Company Events'),
        ('bi-stars', 'Socials'),
        ('bi-camera', 'Photo/Video'),
        ('bi-music-note', 'Entertainment'),
        ('bi-cup-hot', 'Catering'),
        ('bi-flower1', 'Floral'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='bi-stars', choices=ICON_CHOICES)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Amenity(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Amenities'

    def __str__(self):
        return self.name


class AmenityImage(models.Model):
    facility = models.ForeignKey(Amenity, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='amenities/')

    def __str__(self):
        return f"Image for {self.facility.name}"


class ManagementTeam(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Management Team Member'

    def __str__(self):
        return f"{self.name} — {self.role}"