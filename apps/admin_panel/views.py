from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Sum, Count
from django.db.models.functions import TruncWeek, TruncMonth, TruncYear
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings as django_settings
import datetime

from apps.gallery.models import MediaItem, MediaCategory
from apps.posts.models import Post
from apps.appointments.models import Appointment
from apps.chatbot.models import ChatSession
from apps.core.models import SiteSettings, Inquiry, Service, Amenity, ManagementTeam
from apps.notifications.models import Notification
from apps.events.models import EventRecord


def is_staff(user):
    return user.is_staff

staff_required = user_passes_test(is_staff, login_url='/admin-panel/login/')

def _login_staff(f):
    return login_required(login_url='/admin-panel/login/')(staff_required(f))


# ── DASHBOARD ────────────────────────────────────────────────────────
@_login_staff
def dashboard_view(request):
    return render(request, 'admin_panel/dashboard.html', {
        'total_appointments': Appointment.objects.count(),
        'pending_appointments': Appointment.objects.filter(status='pending').count(),
        'total_media': MediaItem.objects.count(),
        'total_posts': Post.objects.count(),
        'recent_appointments': Appointment.objects.order_by('-created_at')[:5],
    })


# ── ANALYTICS ────────────────────────────────────────────────────────
@_login_staff
def analytics_view(request):
    period = request.GET.get('period', 'monthly')
    events = EventRecord.objects.all()

    total_revenue = events.aggregate(t=Sum('amount_paid'))['t'] or 0
    total_amount = events.aggregate(t=Sum('total_amount'))['t'] or 0
    total_remaining = total_amount - total_revenue
    users_availed = events.values('client_email').distinct().count()

    events_by_type = (
        Appointment.objects.filter(status='completed')
        .values('event_type')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    if period == 'weekly':
        trunc_fn = TruncWeek
    elif period == 'annual':
        trunc_fn = TruncYear
    else:
        trunc_fn = TruncMonth

    revenue_over_time = (
        EventRecord.objects
        .annotate(period=trunc_fn('created_at'))
        .values('period')
        .annotate(revenue=Sum('amount_paid'), event_count=Count('id'))
        .order_by('period')
    )

    event_type_labels = [e['event_type'].replace('_', ' ').title() for e in events_by_type]
    event_type_counts = [e['count'] for e in events_by_type]

    rev_labels, rev_data = [], []
    for row in revenue_over_time:
        if row['period']:
            if period == 'weekly':
                label = row['period'].strftime('Week of %b %d')
            elif period == 'annual':
                label = row['period'].strftime('%Y')
            else:
                label = row['period'].strftime('%b %Y')
            rev_labels.append(label)
            rev_data.append(float(row['revenue'] or 0))

    return render(request, 'admin_panel/analytics.html', {
        'period': period,
        'total_revenue': total_revenue,
        'total_remaining': total_remaining,
        'users_availed': users_availed,
        'total_events': events.count(),
        'event_type_labels': event_type_labels,
        'event_type_counts': event_type_counts,
        'rev_labels': rev_labels,
        'rev_data': rev_data,
    })


# ── MEDIA ─────────────────────────────────────────────────────────────
@_login_staff
def media_list_view(request):
    return render(request, 'admin_panel/media_list.html', {
        'items': MediaItem.objects.select_related('category').all(),
        'categories': MediaCategory.objects.all(),
    })

@_login_staff
def media_upload_view(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        category = MediaCategory.objects.filter(pk=request.POST.get('category')).first()
        for f in files:
            MediaItem.objects.create(
                file=f,
                media_type=request.POST.get('media_type', 'photo'),
                category=category,
                is_featured=request.POST.get('is_featured') == 'on',
                title=request.POST.get('title', ''),
            )
        messages.success(request, f'{len(files)} file(s) uploaded.')
        return redirect('admin_panel:media_list')
    return render(request, 'admin_panel/media_upload.html', {'categories': MediaCategory.objects.all()})

@_login_staff
def media_delete_view(request, pk):
    if request.method == 'POST':
        get_object_or_404(MediaItem, pk=pk).delete()
        messages.success(request, 'Media deleted.')
    return redirect('admin_panel:media_list')


# ── POSTS ─────────────────────────────────────────────────────────────
@_login_staff
def posts_list_view(request):
    return render(request, 'admin_panel/posts_list.html', {'posts': Post.objects.all()})

@_login_staff
def post_create_view(request):
    if request.method == 'POST':
        Post.objects.create(
            title=request.POST.get('title'),
            content=request.POST.get('content'),
            image=request.FILES.get('image'),
            is_published=request.POST.get('is_published') == 'on',
            is_featured=request.POST.get('is_featured') == 'on',
        )
        messages.success(request, 'Post created.')
        return redirect('admin_panel:posts_list')
    return render(request, 'admin_panel/post_form.html', {'post': None})

@_login_staff
def post_edit_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.is_published = request.POST.get('is_published') == 'on'
        post.is_featured = request.POST.get('is_featured') == 'on'
        if request.FILES.get('image'):
            post.image = request.FILES.get('image')
        post.save()
        messages.success(request, 'Post updated.')
        return redirect('admin_panel:posts_list')
    return render(request, 'admin_panel/post_form.html', {'post': post})

@_login_staff
def post_delete_view(request, pk):
    if request.method == 'POST':
        get_object_or_404(Post, pk=pk).delete()
        messages.success(request, 'Post deleted.')
    return redirect('admin_panel:posts_list')


# ── SERVICES ─────────────────────────────────────────────────────────
ICON_CHOICES = Service.ICON_CHOICES

@_login_staff
def services_list_view(request):
    return render(request, 'admin_panel/services_list.html', {'services': Service.objects.all()})

@_login_staff
def service_create_view(request):
    if request.method == 'POST':
        Service.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            icon=request.POST.get('icon', 'bi-stars'),
            order=request.POST.get('order', 0),
            is_active=request.POST.get('is_active') == 'on',
        )
        messages.success(request, 'Service created.')
        return redirect('admin_panel:services_list')
    return render(request, 'admin_panel/service_form.html', {'service': None, 'icon_choices': ICON_CHOICES})

@_login_staff
def service_edit_view(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.name = request.POST.get('name')
        service.description = request.POST.get('description')
        service.icon = request.POST.get('icon', 'bi-stars')
        service.order = request.POST.get('order', 0)
        service.is_active = request.POST.get('is_active') == 'on'
        service.save()
        messages.success(request, 'Service updated.')
        return redirect('admin_panel:services_list')
    return render(request, 'admin_panel/service_form.html', {'service': service, 'icon_choices': ICON_CHOICES})

@_login_staff
def service_delete_view(request, pk):
    if request.method == 'POST':
        get_object_or_404(Service, pk=pk).delete()
        messages.success(request, 'Service deleted.')
    return redirect('admin_panel:services_list')


# ── AMENITIES ────────────────────────────────────────────────────────
@_login_staff
def amenities_list_view(request):
    return render(request, 'admin_panel/amenities_list.html', {'facilities': Amenity.objects.all()})

@_login_staff
def amenity_create_view(request):
    if request.method == 'POST':
        Amenity.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description', ''),
            order=request.POST.get('order', 0),
            is_featured=request.POST.get('is_featured') == 'on',
        )
        messages.success(request, 'Amenity created.')
        return redirect('admin_panel:amenities_list')
    return render(request, 'admin_panel/amenity_form.html', {'facility': None})

@_login_staff
def amenity_edit_view(request, pk):
    facility = get_object_or_404(Amenity, pk=pk)
    if request.method == 'POST':
        facility.name = request.POST.get('name')
        facility.description = request.POST.get('description', '')
        facility.order = request.POST.get('order', 0)
        facility.is_featured = request.POST.get('is_featured') == 'on'
        facility.save()
        messages.success(request, 'Amenity updated.')
        return redirect('admin_panel:amenities_list')
    return render(request, 'admin_panel/amenity_form.html', {'facility': facility})

@_login_staff
def amenity_delete_view(request, pk):
    if request.method == 'POST':
        get_object_or_404(Amenity, pk=pk).delete()
        messages.success(request, 'Amenity deleted.')
    return redirect('admin_panel:amenities_list')


# ── TEAM ──────────────────────────────────────────────────────────────
@_login_staff
def team_list_view(request):
    return render(request, 'admin_panel/team_list.html', {'team': ManagementTeam.objects.all()})

@_login_staff
def team_create_view(request):
    if request.method == 'POST':
        ManagementTeam.objects.create(
            name=request.POST.get('name'),
            role=request.POST.get('role'),
            bio=request.POST.get('bio', ''),
            photo=request.FILES.get('photo'),
            order=request.POST.get('order', 0),
            is_active=request.POST.get('is_active') == 'on',
        )
        messages.success(request, 'Team member added.')
        return redirect('admin_panel:team_list')
    return render(request, 'admin_panel/team_form.html', {'member': None})

@_login_staff
def team_edit_view(request, pk):
    member = get_object_or_404(ManagementTeam, pk=pk)
    if request.method == 'POST':
        member.name = request.POST.get('name')
        member.role = request.POST.get('role')
        member.bio = request.POST.get('bio', '')
        member.order = request.POST.get('order', 0)
        member.is_active = request.POST.get('is_active') == 'on'
        if request.FILES.get('photo'):
            member.photo = request.FILES.get('photo')
        member.save()
        messages.success(request, 'Team member updated.')
        return redirect('admin_panel:team_list')
    return render(request, 'admin_panel/team_form.html', {'member': member})

@_login_staff
def team_delete_view(request, pk):
    if request.method == 'POST':
        get_object_or_404(ManagementTeam, pk=pk).delete()
        messages.success(request, 'Team member deleted.')
    return redirect('admin_panel:team_list')


# ── APPOINTMENTS ──────────────────────────────────────────────────────
@_login_staff
def appointments_list_view(request):
    status = request.GET.get('status', '')
    appts = Appointment.objects.all()
    if status:
        appts = appts.filter(status=status)
    completed_with_event = set(
        EventRecord.objects.values_list('appointment_id', flat=True)
    )
    return render(request, 'admin_panel/appointments_list.html', {
        'appointments': appts,
        'status_filter': status,
        'appt_statuses': Appointment.STATUS_CHOICES,
        'completed_with_event': completed_with_event,
    })

@_login_staff
def appointment_detail_view(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        old_status = appt.status
        new_status = request.POST.get('status', appt.status)
        appt.status = new_status
        appt.admin_notes = request.POST.get('admin_notes', appt.admin_notes)
        appt.save()

        if old_status != new_status:
            Notification.objects.create(
                title=f'Appointment Updated — {appt.client_name}',
                message=f'Status changed from {old_status} to {new_status} for {appt.client_name} ({appt.get_event_type_display()}).',
                notif_type='appointment_updated',
                related_appointment_id=appt.pk,
            )

        messages.success(request, 'Appointment updated.')

        if new_status == 'completed':
            if hasattr(appt, 'event_record'):
                return redirect('admin_panel:event_detail', pk=appt.event_record.pk)
            return redirect('admin_panel:event_create', appt_pk=appt.pk)

        return redirect('admin_panel:appointments_list')
    return render(request, 'admin_panel/appointment_detail.html', {'appt': appt})


# ── EVENT RECORDS ─────────────────────────────────────────────────────
@_login_staff
def events_list_view(request):
    events = EventRecord.objects.select_related('appointment').all()
    return render(request, 'admin_panel/events_list.html', {'events': events})

@_login_staff
def event_create_view(request, appt_pk):
    appt = get_object_or_404(Appointment, pk=appt_pk)
    if hasattr(appt, 'event_record'):
        return redirect('admin_panel:event_detail', pk=appt.event_record.pk)

    amenities_list = Amenity.objects.all()

    if request.method == 'POST':
        total = float(request.POST.get('total_amount', 0) or 0)
        paid = float(request.POST.get('amount_paid', 0) or 0)
        payment_type = request.POST.get('payment_type', 'down_payment')
        if payment_type == 'fully_paid':
            paid = total

        event = EventRecord.objects.create(
            appointment=appt,
            client_name=appt.client_name,
            client_email=appt.client_email,
            client_phone=appt.client_phone,
            event_type=appt.get_event_type_display(),
            scheduled_date=request.POST.get('scheduled_date'),
            amenities=request.POST.get('amenities', ''),
            no_of_guests=request.POST.get('no_of_guests', 0),
            special_request=request.POST.get('special_request', ''),
            payment_type=payment_type,
            total_amount=total,
            amount_paid=paid,
        )

        Notification.objects.create(
            title=f'Event Scheduled — {event.client_name}',
            message=f'Event record created for {event.client_name} ({event.event_type}) on {event.scheduled_date}.',
            notif_type='new_appointment',
            related_event_id=event.pk,
        )

        if not event.is_fully_paid:
            _send_payment_reminder(event)

        messages.success(request, 'Event record saved successfully.')
        return redirect('admin_panel:event_detail', pk=event.pk)

    return render(request, 'admin_panel/event_form.html', {
        'appt': appt,
        'amenities_list': amenities_list,
        'today': datetime.date.today(),
    })

@_login_staff
def event_detail_view(request, pk):
    event = get_object_or_404(EventRecord, pk=pk)
    amenities_list = Amenity.objects.all()

    if request.method == 'POST':
        total = float(request.POST.get('total_amount', event.total_amount) or 0)
        payment_type = request.POST.get('payment_type', event.payment_type)
        paid = float(request.POST.get('amount_paid', event.amount_paid) or 0)
        if payment_type == 'fully_paid':
            paid = total

        event.scheduled_date = request.POST.get('scheduled_date', event.scheduled_date)
        event.amenities = request.POST.get('amenities', event.amenities)
        event.no_of_guests = request.POST.get('no_of_guests', event.no_of_guests)
        event.special_request = request.POST.get('special_request', event.special_request)
        event.payment_type = payment_type
        event.total_amount = total
        event.amount_paid = paid
        event.save()

        if not event.is_fully_paid:
            _send_payment_reminder(event)

        messages.success(request, 'Event record updated.')
        return redirect('admin_panel:event_detail', pk=event.pk)

    return render(request, 'admin_panel/event_detail.html', {
        'event': event,
        'amenities_list': amenities_list,
    })


def _send_payment_reminder(event):
    remaining = event.remaining_balance
    subject = f'Payment Reminder — {event.event_type} on {event.scheduled_date}'
    client_msg = (
        f'Dear {event.client_name},\n\n'
        f'This is a friendly reminder that your event "{event.event_type}" '
        f'scheduled on {event.scheduled_date} has an outstanding balance.\n\n'
        f'Total Amount: P{event.total_amount:,.2f}\n'
        f'Amount Paid: P{event.amount_paid:,.2f}\n'
        f'Remaining Balance: P{remaining:,.2f}\n\n'
        f'Please settle your balance before the event date.\n\n'
        f'Thank you,\nKakahoyan Venue'
    )
    try:
        send_mail(subject, client_msg, django_settings.DEFAULT_FROM_EMAIL,
                  [event.client_email], fail_silently=True)
    except Exception:
        pass

    Notification.objects.create(
        title=f'Payment Reminder Sent — {event.client_name}',
        message=f'Reminder sent to {event.client_email}. Remaining balance: P{remaining:,.2f} for {event.event_type} on {event.scheduled_date}.',
        notif_type='payment_reminder',
        related_event_id=event.pk,
    )
    event.reminder_sent_at = timezone.now()
    event.save(update_fields=['reminder_sent_at'])


# ── INQUIRIES / CHATBOT LOGS ──────────────────────────────────────────
@_login_staff
def inquiries_list_view(request):
    return render(request, 'admin_panel/inquiries_list.html', {
        'sessions': ChatSession.objects.prefetch_related('messages').order_by('-created_at')[:50],
    })


# ── SITE SETTINGS ─────────────────────────────────────────────────────
@_login_staff
def site_settings_view(request):
    site = SiteSettings.objects.first()
    if not site:
        site = SiteSettings.objects.create()
    if request.method == 'POST':
        site.venue_name = request.POST.get('venue_name', site.venue_name)
        site.tagline = request.POST.get('tagline', '')
        site.hero_description = request.POST.get('hero_description', '')
        site.phone = request.POST.get('phone', site.phone)
        site.email = request.POST.get('email', '')
        site.hours = request.POST.get('hours', '')
        site.address = request.POST.get('address', site.address)
        site.facebook_url = request.POST.get('facebook_url', '')
        site.google_maps_embed = request.POST.get('google_maps_embed', '')
        site.max_indoor_capacity = request.POST.get('max_indoor_capacity', 250)
        site.max_outdoor_capacity = request.POST.get('max_outdoor_capacity', 500)
        site.save()
        messages.success(request, 'Site settings saved.')
        return redirect('admin_panel:site_settings')
    return render(request, 'admin_panel/site_settings.html', {'site': site})
