"""
Serilizer for API related User
"""

import logging
from datetime import timezone

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.forms import ValidationError
from django.forms.models import model_to_dict

from advertisements.serializers import AdSerializer
from .validators import ValidatorForRegistration


User = get_user_model()
logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user
    """

    class Meta:
        model = User
        fields = (
            "username",
            "password",
        )

    def validate(self, attrs):
        """
        Validate username and password using custom validators
        """
        request = self.context["request"]
        if request.method == "POST":
            try:
                fields = request.data
                list_fields = list(fields.items())
                for field in list_fields:
                    ValidatorForRegistration.validate_field(field)
            except ValidationError as e:
                logger.info("Валидация не прошла")
                raise serializers.ValidationError({"error": str(e)})
            logger.info("Валидация прошла успешно")
        return attrs

    def to_representation(self, instance):
        data = {
            "id": instance.id,
            "username": instance.username,
            "avatar": instance.avatar,
            "description": instance.description,
        }

        request = self.context["request"]
        user_request = request.user
        if instance != user_request:
            data["in_subs"] = instance in user_request.subscriptions.all()

        if ads := [
            {
                **AdSerializer(ad, context={"request": request}).data,
                "in_fav": ad in instance.favorites.all(),
                "created_at": ad.created_at.astimezone(timezone.utc).strftime(
                    "%d %B %Y г. %H:%M"
                ),
            }
            for ad in instance.advertisements.all()
        ]:
            data["ads"] = ads

        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        print(validated_data)
        return user

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get("avatar", instance.avatar)
        instance.description = validated_data.get("description", instance.description)
        instance.username = validated_data.get("username", instance.username)
        instance.save()
        return instance
