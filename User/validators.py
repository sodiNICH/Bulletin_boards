"""
Module with custom validators
"""
import re
import logging

from django.forms import ValidationError
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework import status

User = get_user_model()
logger = logging.getLogger(__name__)


class ValidatorsObjectRegister:
    """
    Object for custom validators
    """

    def validate_field(self, post_request_data: dict):
        """
        Validator for password or username
        """
        field_name, field_value = list(post_request_data.items())[0]
        return self.validator_response(field_name, field_value)

    def validator_response(self, field_name, field_value):
        """
        Return a validator response
        """
        try:
            match field_name:
                case "password":
                    self.password(field_value)
                case "username":
                    self.username(field_value)
                case "email":
                    self.email(field_value)

            return Response(
                data={"message": "Данные введенны корректно"},
                status=status.HTTP_200_OK,
            )
        except ValidationError as e:
            return Response(
                data={
                    "error": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    @staticmethod
    def password(password):
        """
        Method with checking password
        """
        if not password:
            raise ValidationError("Пароль не может быть пустым")

        if len(password) < 8:
            raise ValidationError("Пароль должен содержать не менее 8 символов")

        if not any(char.isdigit() for char in password):
            raise ValidationError("Пароль должен содержать хотя бы одну цифру.")

        if not any(char.islower() for char in password):
            raise ValidationError(
                "Пароль должен содержать хотя бы одну букву в нижнем регистре."
            )

        if not any(char.isupper() for char in password):
            raise ValidationError(
                "Пароль должен содержать хотя бы одну букву в верхнем регистре."
            )

        special_characters = "!@#$%^&*()-_+=[]{}|;:'\",.<>/?"
        if not any(char in special_characters for char in password):
            raise ValidationError(
                "Пароль должен содержать хотя бы один специальный символ."
            )

        return True

    @staticmethod
    def username(username):
        """
        Method with checking password
        """
        if not username:
            raise ValidationError("Логин не может быть пустым")

        if len(username) < 4:
            raise ValidationError("Логин должен содержать не менее 4 символов")

        if not re.match(r"^\w+$", username):
            raise ValidationError(
                "Логин должен содержать только буквы, цифры и символы подчеркивания"
            )

        if User.objects.filter(username=username).exists():
            raise ValidationError("Этот логин уже существует")

        return True

    @staticmethod
    def email(email):
        """
        Method with checking email
        """
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValidationError("Неверный формат для email")
