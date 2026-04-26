from django.db import models


class Inquiry(models.Model):
    STATUS = [('new', 'New'), ('read', 'Read'), ('replied', 'Replied')]
    name       = models.CharField(max_length=200)
    email      = models.EmailField()
    phone      = models.CharField(max_length=20, blank=True)
    subject    = models.CharField(max_length=300)
    message    = models.TextField()
    status     = models.CharField(max_length=10, choices=STATUS, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Inquiries'

    def __str__(self):
        return f"{self.name} — {self.subject}"


class SiteSettings(models.Model):
    venue_name           = models.CharField(max_length=100, default='Kakahoyan')
    tagline              = models.CharField(max_length=300, blank=True)
    phone                = models.CharField(max_length=20, default='0920 611 2718')
    email                = models.EmailField(blank=True)
    address              = models.TextField(default='Purok 2, Brgy. Caranoche, Sta. Catalina, Negros Oriental, 6220')
    facebook_url         = models.URLField(blank=True)
    google_maps_embed    = models.TextField(blank=True, help_text='Full Google Maps embed iframe code')
    max_indoor_capacity  = models.PositiveIntegerField(default=250)
    max_outdoor_capacity = models.PositiveIntegerField(default=500)
    hero_description     = models.TextField(
        default='Kakahoyan offers an exclusive venue for weddings, celebrations, and gatherings — featuring a fully air-conditioned Glass Pavilion for up to 250 guests and a stunning outdoor platform.',
        blank=True
    )
    hours = models.CharField(max_length=100, default='Always open for inquiries', blank=True)

    class Meta:
        verbose_name        = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return 'Site Settings'


class Service(models.Model):
    ICON_CHOICES = [
        ('bi-hearts',      'Hearts (Weddings)'),
        ('bi-balloon',     'Balloon (Birthdays)'),
        ('bi-people',      'People (Reunions)'),
        ('bi-mortarboard', 'Mortarboard (Graduation)'),
        ('bi-briefcase',   'Briefcase (Company Events)'),
        ('bi-stars',       'Stars (Socials)'),
        ('bi-music-note',  'Music Note'),
        ('bi-camera',      'Camera'),
        ('bi-cup-hot',     'Cup (Catering)'),
        ('bi-building',    'Building'),
    ]
    name        = models.CharField(max_length=100)
    description = models.TextField()
    icon        = models.CharField(max_length=50, choices=ICON_CHOICES, default='bi-stars')
    is_active   = models.BooleanField(default=True)
    order       = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Facility(models.Model):
    name        = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)
    order       = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Facilities'

    def __str__(self):
        return self.name


class FacilityImage(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='images')
    image    = models.ImageField(upload_to='facilities/')
    caption  = models.CharField(max_length=200, blank=True)
    order    = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.facility.name} — image #{self.order}"


class ManagementTeam(models.Model):
    name     = models.CharField(max_length=150)
    role     = models.CharField(max_length=150)
    photo    = models.ImageField(upload_to='team/', blank=True, null=True)
    bio      = models.TextField(blank=True)
    order    = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} — {self.role}"
