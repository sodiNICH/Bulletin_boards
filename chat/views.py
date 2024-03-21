import logging

from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser

from .models import Chat, Message
from .serializers import (
    ChatMessageSerializer,
    ChatSerializer,
)
from .tasks import delete_chat_message


logger = logging.getLogger(__name__)


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (JSONParser,)

    def destroy(self, request, *args, **kwargs):
        chat_object = get_object_or_404(Chat, pk=kwargs.get("pk"))
        user = request.user
        user.chats.remove(chat_object)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = ChatMessageSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (
        JSONParser,
        MultiPartParser,
    )

    def get_permissions(self):
        logger.debug(self.action)
        if self.action == "list":
            return (permissions.IsAdminUser(), )
        return super().get_permissions()

    def destroy(self, request, *args, **kwargs):
        message_object = get_object_or_404(self.get_queryset(), pk=kwargs.get("pk"))
        message_owner_id = message_object.owner.id
        if request.user.id == message_owner_id:

            name_group = f"chat_{message_object.chat.id}"
            delete_chat_message.delay(name_group, message_object.id)

            return super().destroy(request, *args, **kwargs)
        return Response(
            data={
                "error": "You can't delete someone else's post!",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
