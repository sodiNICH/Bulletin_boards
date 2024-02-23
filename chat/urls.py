from django.urls import path

from . import views


urlpatterns = [
    # API endpoints
    path("api/v1/list/", views.ChatsListAPIView.as_view(), name="list-chats"),
    path("api/v1/create/", views.ChatCreateAPIView.as_view(), name="create-chat"),
    path("api/v1/<int:pk>/", views.ChatDetailAPIView.as_view(), name="detail-chat"),
    path("api/v1/message/create/", views.CreateMessageChatAPIView.as_view(), name="create-message"),
]
