from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from apps.gallery.models import MediaItem, MediaCategory
from apps.posts.models import Post, PostMedia
from apps.appointments.models import Appointment
from apps.chatbot.models import ChatSession, ChatMessage
from apps.core.models import SiteSettings, Service, Facility, FacilityImage, ManagementTeam


def is_staff(user):
    return user.is_staff

staff_required = user_passes_test(is_staff, login_url='/admin-panel/login/')


@login_required(login_url='/admin-panel/login/')
@staff_required
def dashboard_view(request):
    context = {
        'total_appointments':   Appointment.objects.count(),
        'pending_appointments': Appointment.objects.filter(status='pending').count(),
        'total_media':          MediaItem.objects.count(),
        'total_posts':          Post.objects.count(),
        'recent_appointments':  Appointment.objects.order_by('-created_at')[:5],
    }
    return render(request, 'admin_panel/dashboard.html', context)


# ── Media ────────────────────────────────────────────────────────────

@login_required(login_url='/admin-panel/login/')
@staff_required
def media_list_view(request):
    items      = MediaItem.objects.select_related('category').all()
    categories = MediaCategory.objects.all()
    return render(request, 'admin_panel/media_list.html', {'items': items, 'categories': categories})


@login_required(login_url='/admin-panel/login/')
@staff_required
def media_upload_view(request):
    if request.method == 'POST':
        files      = request.FILES.getlist('files')
        media_type = request.POST.get('media_type', 'photo')
        category_id = request.POST.get('category')
        is_featured = request.POST.get('is_featured') == 'on'
        category = MediaCategory.objects.filter(pk=category_id).first() if category_id else None
        for f in files:
            MediaItem.objects.create(
                file=f, media_type=media_type,
                category=category, is_featured=is_featured,
                title=request.POST.get('title', ''),
            )
        messages.success(request, f'{len(files)} file(s) uploaded successfully.')
        return redirect('admin_panel:media_list')
    categories = MediaCategory.objects.all()
    return render(request, 'admin_panel/media_upload.html', {'categories': categories})


@login_required(login_url='/admin-panel/login/')
@staff_required
def media_delete_view(request, pk):
    item = get_object_or_404(MediaItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Media deleted.')
    return redirect('admin_panel:media_list')


# ── Posts ────────────────────────────────────────────────────────────

@login_required(login_url='/admin-panel/login/')
@staff_required
def posts_list_view(request):
    posts = Post.objects.all()
    return render(request, 'admin_panel/posts_list.html', {'posts': posts})


@login_required(login_url='/admin-panel/login/')
@staff_required
def post_create_view(request):
    if request.method == 'POST':
        post = Post.objects.create(
            title=request.POST.get('title'),
            content=request.POST.get('content'),
            cover_image=request.FILES.get('cover_image'),
            is_published=request.POST.get('is_published') == 'on',
            is_featured=request.POST.get('is_featured') == 'on',
        )
        # Handle multiple media uploads
        files = request.FILES.getlist('media_files')
        for i, f in enumerate(files):
            ext = f.name.lower().split('.')[-1]
            media_type = 'video' if ext in ['mp4', 'mov', 'avi', 'webm'] else 'image'
            PostMedia.objects.create(post=post, file=f, media_type=media_type, order=i)
        messages.success(request, 'Post created successfully.')
        return redirect('admin_panel:posts_list')
    return render(request, 'admin_panel/post_form.html', {'post': None})


@login_required(login_url='/admin-panel/login/')
@staff_required
def post_edit_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.title       = request.POST.get('title')
        post.content     = request.POST.get('content')
        post.is_published = request.POST.get('is_published') == 'on'
        post.is_featured  = request.POST.get('is_featured') == 'on'
        if request.FILES.get('cover_image'):
            post.cover_image = request.FILES.get('cover_image')
        post.save()
        # Add new media files
        files = request.FILES.getlist('media_files')
        for i, f in enumerate(files):
            ext = f.name.lower().split('.')[-1]
            media_type = 'video' if ext in ['mp4', 'mov', 'avi', 'webm'] else 'image'
            PostMedia.objects.create(post=post, file=f, media_type=media_type, order=post.media_files.count() + i)
        # Handle deleted media
        delete_ids = request.POST.getlist('delete_media')
        if delete_ids:
            PostMedia.objects.filter(pk__in=delete_ids, post=post).delete()
        messages.success(request, 'Post updated.')
        return redirect('admin_panel:posts_list')
    return render(request, 'admin_panel/post_form.html', {'post': post})


@login_required(login_url='/admin-panel/login/')
@staff_required
def post_delete_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted.')
    return redirect('admin_panel:posts_list')


# ── Appointments ─────────────────────────────────────────────────────

@login_required(login_url='/admin-panel/login/')
@staff_required
def appointments_list_view(request):
    status = request.GET.get('status', '')
    appts  = Appointment.objects.all()
    if status:
        appts = appts.filter(status=status)
    return render(request, 'admin_panel/appointments_list.html', {
        'appointments': appts,
        'status_filter': status,
        'appt_statuses': Appointment.STATUS_CHOICES,
    })


@login_required(login_url='/admin-panel/login/')
@staff_required
def appointment_detail_view(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appt.status      = request.POST.get('status', appt.status)
        appt.admin_notes = request.POST.get('admin_notes', appt.admin_notes)
        appt.save()
        messages.success(request, 'Appointment updated.')
        return redirect('admin_panel:appointments_list')
    return render(request, 'admin_panel/appointment_detail.html', {'appt': appt})


@login_required(login_url='/admin-panel/login/')
@staff_required
def inquiries_list_view(request):
    sessions = ChatSession.objects.prefetch_related('messages').order_by('-created_at')[:50]
    return render(request, 'admin_panel/inquiries_list.html', {'sessions': sessions})


# ── Site Settings ─────────────────────────────────────────────────────

@login_required(login_url='/admin-panel/login/')
@staff_required
def site_settings_view(request):
    site = SiteSettings.objects.first()
    if not site:
        site = SiteSettings.objects.create()
    if request.method == 'POST':
        site.venue_name           = request.POST.get('venue_name', site.venue_name)
        site.tagline              = request.POST.get('tagline', site.tagline)
        site.hero_description     = request.POST.get('hero_description', site.hero_description)
        site.phone                = request.POST.get('phone', site.phone)
        site.email                = request.POST.get('email', site.email)
        site.address              = request.POST.get('address', site.address)
        site.facebook_url         = request.POST.get('facebook_url', site.facebook_url)
        site.hours                = request.POST.get('hours', site.hours)
        site.max_indoor_capacity  = request.POST.get('max_indoor_capacity', site.max_indoor_capacity)
        site.max_outdoor_capacity = request.POST.get('max_outdoor_capacity', site.max_outdoor_capacity)
        site.google_maps_embed    = request.POST.get('google_maps_embed', site.google_maps_embed)
        site.save()
        messages.success(request, 'Site settings updated.')
        return redirect('admin_panel:site_settings')
    return render(request, 'admin_panel/site_settings.html', {'site': site})


# ── Services ──────────────────────────────────────────────────────────

@login_required(login_url='/admin-panel/login/')
@staff_required
def services_list_view(request):
    services = Service.objects.all()
    return render(request, 'admin_panel/services_list.html', {'services': services})


@login_required(login_url='/admin-panel/login/')
@staff_required
def service_create_view(request):
    from apps.core.models import Service as ServiceModel
    ICON_CHOICES = ServiceModel.ICON_CHOICES
    if request.method == 'POST':
        Service.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            icon=request.POST.get('icon', 'bi-stars'),
            is_active=request.POST.get('is_active') == 'on',
            order=request.POST.get('order', 0),
        )
        messages.success(request, 'Service added.')
        return redirect('admin_panel:services_list')
    return render(request, 'admin_panel/service_form.html', {'service': None, 'icon_choices': ICON_CHOICES})


@login_required(login_url='/admin-panel/login/')
@staff_required
def service_edit_view(request, pk):
    from apps.core.models import Service as ServiceModel
    ICON_CHOICES = ServiceModel.ICON_CHOICES
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.name        = request.POST.get('name')
        service.description = request.POST.get('description')
        service.icon        = request.POST.get('icon', service.icon)
        service.is_active   = request.POST.get('is_active') == 'on'
        service.order       = request.POST.get('order', service.order)
        service.save()
        messages.success(request, 'Service updated.')
        return redirect('admin_panel:services_list')
    return render(request, 'admin_panel/service_form.html', {'service': service, 'icon_choices': ICON_CHOICES})


@login_required(login_url='/admin-panel/login/')
@staff_required
def service_delete_view(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Service deleted.')
    return redirect('admin_panel:services_list')


# ── Facilities ────────────────────────────────────────────────────────

@login_required(login_url='/admin-panel/login/')
@staff_required
def facilities_list_view(request):
    facilities = Facility.objects.prefetch_related('images').all()
    return render(request, 'admin_panel/facilities_list.html', {'facilities': facilities})


@login_required(login_url='/admin-panel/login/')
@staff_required
def facility_create_view(request):
    if request.method == 'POST':
        facility = Facility.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description', ''),
            is_featured=request.POST.get('is_featured') == 'on',
            order=request.POST.get('order', 0),
        )
        images = request.FILES.getlist('images')
        for i, img in enumerate(images[:5]):  # max 5
            FacilityImage.objects.create(facility=facility, image=img, order=i)
        messages.success(request, 'Facility added.')
        return redirect('admin_panel:facilities_list')
    return render(request, 'admin_panel/facility_form.html', {'facility': None})


@login_required(login_url='/admin-panel/login/')
@staff_required
def facility_edit_view(request, pk):
    facility = get_object_or_404(Facility, pk=pk)
    if request.method == 'POST':
        facility.name        = request.POST.get('name')
        facility.description = request.POST.get('description', '')
        facility.is_featured = request.POST.get('is_featured') == 'on'
        facility.order       = request.POST.get('order', facility.order)
        facility.save()
        # Add new images (up to 5 total)
        current_count = facility.images.count()
        images = request.FILES.getlist('images')
        for i, img in enumerate(images[:max(0, 5 - current_count)]):
            FacilityImage.objects.create(facility=facility, image=img, order=current_count + i)
        # Delete selected images
        delete_ids = request.POST.getlist('delete_image')
        if delete_ids:
            FacilityImage.objects.filter(pk__in=delete_ids, facility=facility).delete()
        messages.success(request, 'Facility updated.')
        return redirect('admin_panel:facilities_list')
    return render(request, 'admin_panel/facility_form.html', {'facility': facility})


@login_required(login_url='/admin-panel/login/')
@staff_required
def facility_delete_view(request, pk):
    facility = get_object_or_404(Facility, pk=pk)
    if request.method == 'POST':
        facility.delete()
        messages.success(request, 'Facility deleted.')
    return redirect('admin_panel:facilities_list')


# ── Management Team ───────────────────────────────────────────────────

@login_required(login_url='/admin-panel/login/')
@staff_required
def team_list_view(request):
    team = ManagementTeam.objects.all()
    return render(request, 'admin_panel/team_list.html', {'team': team})


@login_required(login_url='/admin-panel/login/')
@staff_required
def team_create_view(request):
    if request.method == 'POST':
        ManagementTeam.objects.create(
            name=request.POST.get('name'),
            role=request.POST.get('role'),
            bio=request.POST.get('bio', ''),
            photo=request.FILES.get('photo'),
            is_active=request.POST.get('is_active') == 'on',
            order=request.POST.get('order', 0),
        )
        messages.success(request, 'Team member added.')
        return redirect('admin_panel:team_list')
    return render(request, 'admin_panel/team_form.html', {'member': None})


@login_required(login_url='/admin-panel/login/')
@staff_required
def team_edit_view(request, pk):
    member = get_object_or_404(ManagementTeam, pk=pk)
    if request.method == 'POST':
        member.name      = request.POST.get('name')
        member.role      = request.POST.get('role')
        member.bio       = request.POST.get('bio', '')
        member.is_active = request.POST.get('is_active') == 'on'
        member.order     = request.POST.get('order', member.order)
        if request.FILES.get('photo'):
            member.photo = request.FILES.get('photo')
        member.save()
        messages.success(request, 'Team member updated.')
        return redirect('admin_panel:team_list')
    return render(request, 'admin_panel/team_form.html', {'member': member})


@login_required(login_url='/admin-panel/login/')
@staff_required
def team_delete_view(request, pk):
    member = get_object_or_404(ManagementTeam, pk=pk)
    if request.method == 'POST':
        member.delete()
        messages.success(request, 'Team member deleted.')
    return redirect('admin_panel:team_list')
