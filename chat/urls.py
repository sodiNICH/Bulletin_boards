from django.urls import include, path

from rest_framework import routers

from . import views, render_templates


router = routers.DefaultRouter()
router.register(
    r"api/v1",
    views.ChatViewSet,
    basename="chat-api"
)
router.register(
    r"message/api/v1",
    views.MessageViewSet,
    basename="message-chat-api",
)

urlpatterns = [
    # Template endpoints
    path("", render_templates.ListChatsTemplate.as_view(), name="list-chats-template"),
    path("<int:pk>/", render_templates.DetailChatTemplate.as_view(), name="detail-chat-template"),
    # API endpoints
    path("", include(router.urls)),
]
