from django.conf import settings


def site_settings(request):
    ctx = {
        "SITE_NAME": settings.SITE_NAME,
    }
    if hasattr(request, "user") and request.user.is_authenticated:
        from .models import Notification
        ctx["unread_notification_count"] = Notification.objects.filter(
            recipient=request.user, is_read=False
        ).count()
    return ctx
