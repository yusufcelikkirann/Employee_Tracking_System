# employee/signals.py

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser

# Signal to send notification when annual leave is less than 3
# @receiver(pre_save, sender=CustomUser)
# def notify_admin_on_low_leave(sender, instance, **kwargs):
#     if instance.annual_leave < 3:
#         # Send an email to the admin (you can also send a notification)
#         send_mail(
#             'Low Annual Leave Warning',
#             f'User {instance.username} has less than 3 days of annual leave remaining.',
#             settings.DEFAULT_FROM_EMAIL,
#             [settings.ADMIN_EMAIL],  # Make sure to configure this in your settings
#         )
