from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from apps.gallery.models import MediaItem, MediaCategory
from apps.posts.models import Post
from apps.appointments.models import Appointment
from apps.chatbot.models import ChatSession, ChatMessage

def is_staff(user):
    return user.is_staff

staff_required = user_passes_test(is_staff, login_url='/admin-panel/login/')

@login_required(login_url='/admin-panel/login/')
@staff_required
def dashboard_view(request):
    context = {
        'total_appointments': Appointment.objects.count(),
        'pending_appointments': Appointment.objects.filter(status='pending').count(),
        'total_media': MediaItem.objects.count(),
        'total_posts': Post.objects.count(),
        'recent_appointments': Appointment.objects.order_by('-created_at')[:5],
    }
    return render(request, 'admin_panel/dashboard.html', context)

@login_required(login_url='/admin-panel/login/')
@staff_required
def media_list_view(request):
    items = MediaItem.objects.select_related('category').all()
    categories = MediaCategory.objects.all()
    return render(request, 'admin_panel/media_list.html', {'items': items, 'categories': categories})

@login_required(login_url='/admin-panel/login/')
@staff_required
def media_upload_view(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
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

@login_required(login_url='/admin-panel/login/')
@staff_required
def posts_list_view(request):
    posts = Post.objects.all()
    return render(request, 'admin_panel/posts_list.html', {'posts': posts})

@login_required(login_url='/admin-panel/login/')
@staff_required
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

@login_required(login_url='/admin-panel/login/')
@staff_required
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

@login_required(login_url='/admin-panel/login/')
@staff_required
def post_delete_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted.')
    return redirect('admin_panel:posts_list')

@login_required(login_url='/admin-panel/login/')
@staff_required
def appointments_list_view(request):
    status = request.GET.get('status', '')
    appts = Appointment.objects.all()
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
        appt.status = request.POST.get('status', appt.status)
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
