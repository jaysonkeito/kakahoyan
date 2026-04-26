from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from apps.gallery.models import MediaItem
from apps.posts.models import Post
from .models import SiteSettings, Service, Facility, ManagementTeam


def _get_site():
    try:
        return SiteSettings.objects.first()
    except Exception:
        return None


def home(request):
    featured_media = MediaItem.objects.filter(is_featured=True)[:7]
    recent_posts   = Post.objects.filter(is_published=True)[:3]
    services       = Service.objects.filter(is_active=True)
    return render(request, 'core/home.html', {
        'featured_media': featured_media,
        'recent_posts':   recent_posts,
        'site':           _get_site(),
        'services':       services,
    })


def about(request):
    return render(request, 'core/about.html', {'site': _get_site()})


def packages(request):
    services = Service.objects.filter(is_active=True)
    return render(request, 'core/packages.html', {
        'site':     _get_site(),
        'services': services,
    })


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
