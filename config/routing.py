from django.urls import re_path

from notification.consumers import NotificationConsumer
from chat.consumers import ChatConsumer


websocket_urlpatterns = [
    re_path(
        r"ws/notifications/subscriptions/$",
        NotificationConsumer.as_asgi(),
    ),
    re_path(
        r"ws/chat/(?P<chat_id>\d+)/$",
        ChatConsumer.as_asgi(),
    ),
]
