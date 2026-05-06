from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Appointment
from apps.notifications.models import Notification


@receiver(post_save, sender=Appointment)
def appointment_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            title=f'New Appointment — {instance.client_name}',
            message=f'{instance.client_name} requested a {instance.get_event_type_display()} appointment on {instance.discussion_date}.',
            notif_type='new_appointment',
            related_appointment_id=instance.pk,
        )
