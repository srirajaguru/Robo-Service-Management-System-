from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from accounts.decorators import staff_required, admin_required
from .models import Notification
from .services.whatsapp import send_whatsapp_notification


@staff_required
def notification_list(request):
    notifications = Notification.objects.select_related('service', 'customer', 'sent_by').all()
    status_filter = request.GET.get('status')
    if status_filter:
        notifications = notifications.filter(status=status_filter)
    
    return render(request, 'notification/list.html', {
        'notifications': notifications,
        'status_filter': status_filter,
    })


@staff_required
def notification_resend(request, pk):
    notif = get_object_or_404(Notification, pk=pk)
    staff = getattr(request.user, 'staffprofile', None)
    new_notif = send_whatsapp_notification(
        service=notif.service,
        notification_type=notif.notification_type,
        message=notif.message,
        staff_profile=staff
    )
    if new_notif.status in ('Sent', 'Simulated'):
        messages.success(request, f"Notification retry recorded (Status: {new_notif.get_status_display()}).")
    else:
        messages.warning(request, f"Notification retry failed: {new_notif.response_log}")
    return redirect(request.META.get('HTTP_REFERER', 'notification_list'))
