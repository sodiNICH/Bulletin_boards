from collections import OrderedDict

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Chat, Message


User = get_user_model()


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
        companions = attrs.get("companions", [])
        existing_chat = Chat.objects.filter(companions__in=companions).distinct()
        if existing_chat.exists():
            raise serializers.ValidationError(
                "Chat with these companions already exists."
            )

        user = self.context["request"].user
        if user not in companions:
            raise serializers.ValidationError(
                "You can't create a chat room for unauthorized people"
            )

        companions.remove(user)
        advert = attrs.get("advertisement")
        if advert not in companions[0].advertisements.all():
            raise serializers.ValidationError(
                f"None of the users owns the ad - {advert}"
            )
        companions.append(user)
        return attrs


class ChatDetailSerializer(serializers.ModelSerializer):
    advert = serializers.SerializerMethodField()
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ("id", "advert", "messages")

    def get_advert(self, obj):
        advert = obj.advertisement
        return {"title": advert.title, "images": advert.images[0]}

    def get_messages(self, obj):
        messages = obj.messages.all()
        if messages:
            return ChatMessageSerializer(messages, many=True).data
        return []


class ChatListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"

    def to_representation(self, instance):
        user = self.context["request"].user
        chats = user.chats.all()
        serializer_chats = ChatDetailSerializer(chats, many=True).data
        return serializer_chats


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"

    def create(self, validated_data):
        chat = validated_data["chat"]
        message = super().create(validated_data)
        chat.messages.add(message)
        return message

    def validate(self, attrs):
        chat: Chat = attrs.get("chat")
        owner: User = attrs.get("owner")
        if chat and owner:
            if owner not in chat.companions.all():
                raise ValidationError(f'The user {owner} is not in this chat room')
        return super().validate(attrs)

    def to_representation(self, instance):
        data = OrderedDict(
            {
                "avatar": instance.owner.avatar,
                "username": instance.owner.username,
                "text": instance.text,
                "created_at": instance.created_at,
            }
        )
        return data
