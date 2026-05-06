from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True
    dependencies = [
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE,
                    related_name='event_record', to='appointments.appointment')),
                ('client_name', models.CharField(max_length=200)),
                ('client_email', models.EmailField()),
                ('client_phone', models.CharField(max_length=20)),
                ('event_type', models.CharField(max_length=50)),
                ('scheduled_date', models.DateField()),
                ('amenities', models.TextField(blank=True)),
                ('no_of_guests', models.PositiveIntegerField(default=0)),
                ('special_request', models.TextField(blank=True)),
                ('payment_type', models.CharField(
                    choices=[('down_payment','Down Payment'),('fully_paid','Fully Paid')],
                    default='down_payment', max_length=20)),
                ('total_amount', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('amount_paid', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('reminder_sent_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['scheduled_date']},
        ),
    ]
