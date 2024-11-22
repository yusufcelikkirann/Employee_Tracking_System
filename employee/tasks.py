# tasks.py

from celery import shared_task
from channels.layers import get_channel_layer
from django.contrib.auth.models import User

@shared_task
def notify_admin_of_late_employee(user_id, late_minutes):
    # Kullanıcıyı al
    user = User.objects.get(id=user_id)

    # WebSocket üzerinden bildirim gönder
    channel_layer = get_channel_layer()
    message = f"{user.username} geç kaldı! {late_minutes} dakika geç geldi."

    # Admin'e bildirim gönder
    channel_layer.group_send(
        "admin_notifications",  # Admin grubu
        {
            "type": "send_notification",
            "message": message,
        }
    )
