"""
Serializer for Ad
"""

import logging
from datetime import datetime, timezone

from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Advertisements


User = get_user_model()
logger = logging.getLogger(__name__)


class AdSerializer(serializers.ModelSerializer):
    """
    Serializer for Ad
    """

    class Meta:
        model = Advertisements
        fields = "__all__"
        # read_only_fields = ("created_at",)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        owner = instance.owner
        request = self.context.get("request")
        user = request.user
        data = {
            "created_at": instance.created_at
            .astimezone(timezone.utc)
            .strftime("%d %B %Y г. %H:%M"),
            "owner": {
                "id": owner.id,
                "avatar": owner.avatar,
                "username": owner.username,
            },
            "url": f"/ad/{instance.id}/",
            "in_fav": instance in user.favorites.all()
            if user.is_authenticated
            else None,
        }
        representation.update(data)
        return representation
