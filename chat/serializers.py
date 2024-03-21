import logging
from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from config.minio_utils import MinIOFileManager
from .models import Chat, Message
from .validators import validate_for_create_chat
from .tasks import update_chat_list_via_websocket, update_detail_chat_via_websocket


User = get_user_model()
logger = logging.getLogger(__name__)


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"

    def to_representation(self, instance):
        logger.debug(self.context)
        user = self.context["request"].user
        if instance in user.chats.all():
            logger.debug(user.chats.all())
            advert_obj = instance.advertisement
            messages = instance.messages.all().order_by("created_at")
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
            logger.debug(data)
            return data

    def create(self, validated_data):
        user = self.context["request"].user
        chat_object = super().create(validated_data)
        user.chats.add(chat_object)
        return chat_object

    def validate(self, attrs):
        logger.debug(attrs)
        user: AbstractBaseUser = self.context["request"].user
        validate_for_create_chat(attrs, user)
        return attrs


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"

    def create(self, validated_data):
        request = self.context["request"]
        chat = validated_data["chat"]
        message = super().create(validated_data)
        chat.messages.add(message)

        user = self.context["request"].user

        companions = chat.companions
        companions.remove(user)
        companion = companions.all()[0]
        chats_companion = companion.chats
        if chat not in chats_companion.all():
            chats_companion.add(chat)
            name_group = f"chat_list_{companion.id}"
            update_chat_list_via_websocket.delay(name_group, ChatSerializer(chat, context={"request": request}).data)
        companions.add(user)
        name_group = f"chat_{chat.id}"
        update_detail_chat_via_websocket(name_group, self.to_representation(message))
        return message

    def to_internal_value(self, data):
        logger.debug(data)
        images = data.getlist("images")
        logger.debug(images)
        owner = data.get("owner")

        if images:
            images_urls = []
            for image in images:
                logger.debug(image)
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
                "id": instance.id,
                "user_id": instance.owner.id,
                "avatar": instance.owner.avatar,
                "username": instance.owner.username,
                "text": instance.text,
                "images": instance.images,
                "created_at": instance.created_at.strftime("%d %B %Y г. %H:%M"),
            }
        )
        return data
