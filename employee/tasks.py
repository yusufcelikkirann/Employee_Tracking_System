
from celery import shared_task
from channels.layers import get_channel_layer
from django.contrib.auth.models import User

@shared_task
def notify_admin_of_late_employee(user_id, late_minutes):
    
    user = User.objects.get(id=user_id)

   
    channel_layer = get_channel_layer()
    message = f"{user.username} geç kaldı! {late_minutes} dakika geç geldi."

    
    channel_layer.group_send(
        "admin_notifications",  
        {
            "type": "send_notification",
            "message": message,
        }
    )
