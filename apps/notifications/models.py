from django.db import models
from django.utils import timezone


class Notification(models.Model):
    TYPE_CHOICES = [
        ('new_appointment', 'New Appointment'),
        ('appointment_updated', 'Appointment Updated'),
        ('payment_reminder', 'Payment Reminder'),
        ('event_upcoming', 'Event Upcoming'),
        ('system', 'System'),
    ]

    title = models.CharField(max_length=300)
    message = models.TextField()
    notif_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='system')
    is_read = models.BooleanField(default=False)
    related_appointment_id = models.IntegerField(null=True, blank=True)
    related_event_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def mark_read(self):
        self.is_read = True
        self.save(update_fields=['is_read'])
