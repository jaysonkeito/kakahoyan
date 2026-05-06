from django.db import models
from django.utils import timezone
from apps.appointments.models import Appointment


class EventRecord(models.Model):
    PAYMENT_CHOICES = [
        ('down_payment', 'Down Payment'),
        ('fully_paid', 'Fully Paid'),
    ]

    appointment = models.OneToOneField(
        Appointment, on_delete=models.CASCADE, related_name='event_record'
    )

    # Auto from appointment
    client_name = models.CharField(max_length=200)
    client_email = models.EmailField()
    client_phone = models.CharField(max_length=20)
    event_type = models.CharField(max_length=50)

    # Admin fills
    scheduled_date = models.DateField()
    amenities = models.TextField(blank=True, help_text='Amenities included for the event')
    no_of_guests = models.PositiveIntegerField(default=0)
    special_request = models.TextField(blank=True)

    # Payment
    payment_type = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='down_payment')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Reminder tracking
    reminder_sent_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['scheduled_date']

    def __str__(self):
        return f"{self.client_name} — {self.event_type} on {self.scheduled_date}"

    @property
    def remaining_balance(self):
        return self.total_amount - self.amount_paid

    @property
    def is_fully_paid(self):
        return self.payment_type == 'fully_paid' or self.remaining_balance <= 0
