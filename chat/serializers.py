import logging
from datetime import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from config.minio_utils import MinIOFileManager
from .models import Chat, Message
from .validators import validate_for_create_chat


User = get_user_model()
logger = logging.getLogger(__name__)


class ChatCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"

    def create(self, validated_data):
        user = self.context["request"].user
        chat_object = super().create(validated_data)
        user.chats.add(chat_object)
        return chat_object

    def validate(self, attrs):
        user: AbstractBaseUser = self.context["request"].user
        validate_for_create_chat(attrs, user)
        return attrs


class ChatDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ("id", "advertisement", "messages")

    def to_representation(self, instance):
        user = self.context["request"].user
        if instance in user.chats.all():
            logger.debug(user.chats.all())
            advert_obj = instance.advertisement
            messages = instance.messages.all()
            data = {
                "id": instance.id,
                "advert": {
                    "id": advert_obj.id,
                    "title": advert_obj.title,
                    "images": advert_obj.images[0],
                },
                "messages": ChatMessageSerializer(messages, many=True).data
                if messages
                else None,
            }
            return OrderedDict(data)


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        # exclude = ("images",)
        fields = "__all__"

    def create(self, validated_data):
        chat = validated_data["chat"]
        message = super().create(validated_data)
        chat.messages.add(message)

        user = self.context["request"].user
        companions = chat.companions
        logger.debug(companions)
        companions.remove(user)

        chats_companion = companions.all()[0].chats
        if chat not in chats_companion.all():
            chats_companion.add(chat)
        companions.add(user)

        channel_layer = get_channel_layer()
        name_group = f"chat_{chat.id}"
        async_to_sync(channel_layer.group_send)(
            name_group,
            {
                "type": "send_message_chat",
                "message": self.to_representation(message),
            }
        )
        return message

    def to_internal_value(self, data):
        logger.debug(data)
        images = data.getlist("images")
        owner = data.get("owner")

        if images:
            images_urls = []
            for image in images:
                file_name = f"{owner}-{image.name}"
                MinIOFileManager.upload_to_minio(image, f"{owner}-{image.name}")
                images_urls.append(f"/media/{file_name}/")
            data.setlist("images", images_urls)
        return super().to_internal_value(data)

    def validate(self, attrs):
        chat: Chat = attrs.get("chat")
        owner: User = attrs.get("owner")
        print(attrs.get("images"))
        if chat and owner:
            if owner not in chat.companions.all():
                raise ValidationError(f"The user {owner} is not in this chat room")
        return super().validate(attrs)

    def to_representation(self, instance):
        data = OrderedDict(
            {
                "id": instance.owner.id,
                "avatar": instance.owner.avatar,
                "username": instance.owner.username,
                "text": instance.text,
                "images": instance.images,
                "created_at": instance.created_at.strftime("%d %B %Y г. %H:%M"),
            }
        )
        return data
