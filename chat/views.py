from rest_framework import permissions, generics
from rest_framework.parsers import JSONParser, MultiPartParser

from .models import Chat, Message
from .serializers import (
    ChatListSerializer,
    ChatCreateSerializer,
    ChatMessageSerializer,
    ChatDetailSerializer,
)


class ChatsListAPIView(generics.ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatListSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ChatDetailAPIView(generics.RetrieveAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ChatCreateAPIView(generics.CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (JSONParser,)


class CreateMessageChatAPIView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = ChatMessageSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (
        JSONParser,
        MultiPartParser,
    )
