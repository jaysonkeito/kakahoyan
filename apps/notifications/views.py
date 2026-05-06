from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from .models import Notification


def is_staff(user):
    return user.is_staff

staff_required = user_passes_test(is_staff, login_url='/admin-panel/login/')

def _login_staff(f):
    return login_required(login_url='/admin-panel/login/')(staff_required(f))


@_login_staff
def notifications_json(request):
    notifs = Notification.objects.order_by('-created_at')[:30]
    unread_count = Notification.objects.filter(is_read=False).count()
    data = {
        'unread_count': unread_count,
        'notifications': [
            {
                'id': n.id,
                'title': n.title,
                'message': n.message,
                'type': n.notif_type,
                'is_read': n.is_read,
                'created_at': n.created_at.strftime('%b %d, %Y %I:%M %p'),
                'related_appointment_id': n.related_appointment_id,
                'related_event_id': n.related_event_id,
            }
            for n in notifs
        ]
    }
    return JsonResponse(data)


@_login_staff
@require_POST
def mark_read(request, pk):
    try:
        n = Notification.objects.get(pk=pk)
        n.mark_read()
        return JsonResponse({'ok': True})
    except Notification.DoesNotExist:
        return JsonResponse({'ok': False}, status=404)


@_login_staff
@require_POST
def mark_all_read(request):
    Notification.objects.filter(is_read=False).update(is_read=True)
    return JsonResponse({'ok': True})
