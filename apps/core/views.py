from django.shortcuts import render, redirect
from django.contrib import messages
from apps.gallery.models import MediaItem
from apps.posts.models import Post
from django.core.mail import send_mail
from django.conf import settings

EVENT_TYPES = [
    ('bi-hearts',      'Weddings',       'Elegant ceremonies in our Glass Pavilion'),
    ('bi-balloon',     'Birthdays',      'Intimate to grand celebrations'),
    ('bi-people',      'Reunions',       'Reconnect with friends & family'),
    ('bi-mortarboard', 'Graduation',     'Celebrate your achievements'),
    ('bi-briefcase',   'Company Events', 'Team building & seminars'),
    ('bi-stars',       'Socials',        'Special gatherings & parties'),
]

def _get_site():
    """Safe helper — returns SiteSettings or None without crashing."""
    try:
        from .models import SiteSettings
        return SiteSettings.objects.first()
    except Exception:
        return None

def home(request):
    featured_media = MediaItem.objects.filter(is_featured=True)[:7]
    recent_posts   = Post.objects.filter(is_published=True)[:3]
    return render(request, 'core/home.html', {
        'featured_media': featured_media,
        'recent_posts':   recent_posts,
        'site':           _get_site(),
        'event_types':    EVENT_TYPES,
    })

def about(request):
    return render(request, 'core/about.html', {'site': _get_site()})

def packages(request):
    pkg_list = [
        ("bi bi-hearts",      "Weddings",       "Elegant ceremonies in our Glass Pavilion with up to 250 guests. Indoor air-conditioned setting with outdoor lawn option."),
        ("bi bi-balloon",     "Birthdays",      "From intimate family celebrations to grand debut parties — we make every birthday memorable."),
        ("bi bi-people",      "Reunions",       "The perfect setting to reconnect with family, batchmates, or old friends. Spacious indoor and outdoor areas."),
        ("bi bi-mortarboard", "Graduation",     "Celebrate academic achievements in style. Perfect for intimate gatherings and big reception parties."),
        ("bi bi-briefcase",   "Company Events", "Team building, seminars, trainings, and corporate parties. Fully air-conditioned with AV-ready spaces."),
        ("bi bi-stars",       "Socials",        "Cocktail nights, despedida parties, holiday socials — any occasion deserves a beautiful venue."),
    ]
    return render(request, "core/packages.html", {"site": _get_site(), "packages": pkg_list})

def contact(request):
    if request.method == 'POST':
        try:
            from .models import Inquiry
            name    = request.POST.get('name')
            email   = request.POST.get('email')
            phone   = request.POST.get('phone', '')
            subject = request.POST.get('subject')
            message = request.POST.get('message')

            Inquiry.objects.create(
                name=name, email=email,
                phone=phone, subject=subject, message=message,
            )

            # Send email to both Jayson and Kakahoyan Gmail
            send_mail(
                subject=f"[Kakahoyan Inquiry] {subject}",
                message=f"From: {name} <{email}>\nPhone: {phone}\n\n{message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[
                    settings.ADMIN_EMAIL,
                    'kakahoyaneventplace@gmail.com',
                ],
                fail_silently=False,
            )

            messages.success(request, 'Your message has been sent! We will get back to you soon.')
        except Exception as e:
            messages.error(request, 'Something went wrong. Please call us at 0920 611 2718.')
        return redirect('contact')
    return render(request, 'core/contact.html', {'site': _get_site()})