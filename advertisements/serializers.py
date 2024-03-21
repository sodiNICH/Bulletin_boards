"""
Serializer for Ad
"""

import logging
from datetime import timezone

from django.contrib.auth import get_user_model

from rest_framework import serializers

from chat.models import Chat
from .models import Advertisements


User = get_user_model()
logger = logging.getLogger(__name__)


class AdSerializer(serializers.ModelSerializer):
    """
    Serializer for Ad
    """

    category_display = serializers.CharField(source="get_category_display")
    subcategory_display = serializers.CharField(source="get_subcategory_display")
    condition = serializers.CharField(source="get_condition_display")
    created_at = serializers.DateTimeField(
        default_timezone=timezone.utc, format="%d %B %Y г. %H:%M"
    )


    class Meta:
        model = Advertisements
        fields = "__all__"
        # read_only_fields = ("created_at",)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        owner = instance.owner
        request = self.context.get("request")
        user = request.user

        companions_chat = [user.id, instance.owner.id]
        existing_chat = Chat.objects.filter(
            companions__in=companions_chat, advertisement_id=instance.id
        )
        data = {
            "owner": {
                "id": owner.id,
                "avatar": owner.avatar,
                "username": owner.username,
            },
            "url": f"/ad/{instance.id}/",
            "typing": len(existing_chat) > 1,
            "in_fav": instance in user.favorites.all()
            if user.is_authenticated
            else None,
        }
        representation.update(data)
        return representation
