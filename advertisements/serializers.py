"""
Serializer for Ad
"""

import logging

from django.contrib.auth import  get_user_model

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
        read_only_fields = (
            "created_at",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        owner = instance.owner
        request = self.context.get("request")
        user = request.user
        data = {
            "owner": {
                "id": owner.id,
                "username": owner.username,
            },
            "in_fav": instance in user.favorites.all(),
        }
        representation.update(data)
        return representation
