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

        try:
            validator.validate_field(self.context["request"].POST)
            validator.validate_field(self.context["request"].POST)
        except ValidationError as e:
            logger.debug("Валидация не прошла")
            raise serializers.ValidationError({"error": str(e)})
        logger.debug("Валидация прошла успешно")
        return attrs

    def to_representation(self, instance):
        data = {
            "username": instance.username,
            "password": instance.id,
        }
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        print(validated_data)
        return user


class EmailFormSerializer(serializers.Serializer):
    """
    Serializer for email
    """
    email = serializers.EmailField()
