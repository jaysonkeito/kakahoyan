from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import AppointmentForm

def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appt = form.save()
            try:
                send_mail(
                    subject=f'New Appointment Request — {appt.client_name}',
                    message=(
                        f'New appointment from {appt.client_name}\n'
                        f'Phone: {appt.client_phone}\n'
                        f'Email: {appt.client_email}\n'
                        f'Event: {appt.get_event_type_display()}\n'
                        f'Discussion: {appt.discussion_date} at {appt.discussion_time}\n'
                        f'Type: {appt.get_discussion_type_display()}\n'
                        f'Address: {appt.client_address}'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.EMAIL_HOST_USER],
                    fail_silently=True,
                )
            except Exception:
                pass
            return redirect('appointment_success')
    else:
        form = AppointmentForm()

    return render(request, 'appointments/appointment.html', {'form': form})


def appointment_success(request):
    return render(request, 'appointments/success.html')