# employee/routing.py

from django.urls import re_path
from . import consumers  # consumers.py dosyasındaki consumer'ı import ediyoruz

websocket_urlpatterns = [
    re_path(r'^ws/notifications/$', consumers.NotificationConsumer.as_asgi()),  # WebSocket için doğru URL
]
