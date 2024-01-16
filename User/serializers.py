"""
Serilizer for API related User
"""

import logging

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.forms import ValidationError

from .validators import ValidatorsObjectRegister


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
        validator = ValidatorsObjectRegister()

        logger.debug(self.context["request"].data)
        try:
            validator.validate_field(self.context["request"].data)
        except ValidationError as e:
            logger.debug("Валидация не прошла")
            raise serializers.ValidationError({"error": str(e)})
        logger.debug("Валидация прошла успешно")
        return attrs

    def to_representation(self, instance):
        data = {
            "id": instance.id,
            "username": instance.username,
            "avatar": instance.avatar,
            "description": instance.description,
        }
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
