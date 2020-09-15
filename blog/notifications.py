from blog.models import NotifyMe


def mynotifications(user):
    u_notify1 = NotifyMe.objects.filter(user=user).order_by('-date_notified')
    u_notify = NotifyMe.objects.filter(user=user).filter(read=False).order_by('-date_notified')
    u_notify_count = u_notify.count()

    has_new_notification = False
    if u_notify_count > 0:
        has_new_notification = True

    notify_context = {
        "notification": u_notify1,
        "unread_notification": u_notify,
        "u_notify_count": u_notify_count,
        "has_new_notification": has_new_notification,
    }

    return notify_context
