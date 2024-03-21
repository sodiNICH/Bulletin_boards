from django.urls import re_path

from notification.consumers import NotificationConsumer
from chat.consumers import ChatMessageConsumer, ChatListConsumers


websocket_urlpatterns = [
    re_path(
        r"ws/notifications/subscriptions/$",
        NotificationConsumer.as_asgi(),
    ),
    re_path(
        r"ws/chat/list/$",
        ChatListConsumers.as_asgi(),
    ),
    re_path(
        r"ws/chat/(?P<chat_id>\d+)/$",
        ChatMessageConsumer.as_asgi(),
    ),
]
