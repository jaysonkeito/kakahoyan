from django.db import models
from django.utils import timezone

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    DISCUSSION_TYPE = [
        ('at_venue', 'At Kakahoyan Venue'),
        ('client_address', 'Client-specified Address'),
        ('phone_call', 'Phone Call'),
    ]
    EVENT_TYPES = [
        ('wedding', 'Wedding'),
        ('birthday', 'Birthday Party'),
        ('reunion', 'Reunion'),
        ('graduation', 'Graduation Party'),
        ('company', 'Company Event'),
        ('seminar', 'Seminar / Training'),
        ('other', 'Other'),
    ]

    # Client info
    client_name = models.CharField(max_length=200)
    client_email = models.EmailField()
    client_phone = models.CharField(max_length=20)

    # Event details
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    event_date = models.DateField(null=True, blank=True, help_text='Planned event date')
    expected_guests = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True, help_text='Additional details or questions')

    # Discussion appointment
    discussion_date = models.DateField()
    discussion_time = models.TimeField()
    discussion_type = models.CharField(max_length=20, choices=DISCUSSION_TYPE)
    client_address = models.CharField(
        max_length=500, blank=True,
        help_text='Required if discussion type is client-specified address (must be between Sta. Catalina and Bayawan City)'
    )

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.client_name} — {self.get_event_type_display()} on {self.discussion_date}"
