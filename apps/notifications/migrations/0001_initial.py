from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('message', models.TextField()),
                ('notif_type', models.CharField(
                    choices=[('new_appointment','New Appointment'),('appointment_updated','Appointment Updated'),
                             ('payment_reminder','Payment Reminder'),('event_upcoming','Event Upcoming'),('system','System')],
                    default='system', max_length=30)),
                ('is_read', models.BooleanField(default=False)),
                ('related_appointment_id', models.IntegerField(blank=True, null=True)),
                ('related_event_id', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
