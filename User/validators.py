"""
Module with custom validators
"""
import re
import logging

from django.forms import ValidationError
from django.contrib.auth import get_user_model
from django.http import HttpRequest

from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response


User = get_user_model()
logger = logging.getLogger(__name__)


class ValidatorForRegistration:
    """
    Object for custom validators register
    """

    @classmethod
    def validate_field(cls, post_request_data: dict):
        """
        Validator for password or username
        """
        field_name, field_value = post_request_data
        return cls._validator_response(field_name, field_value)

    @classmethod
    def _validator_response(cls, field_name, field_value):
        """
        Return a validator response
        """
        match field_name:
            case "password":
                cls._password(field_value)
            case "username":
                cls._username(field_value)

    @staticmethod
    def _password(password):
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
    def _username(username):
        """
        Method with checking password
        """
        if not username:
            raise ValidationError("Логин не может быть пустым")

        if len(username) < 4:
            print(" ало меньше 4")
            raise ValidationError("Логин должен содержать не менее 4 символов")

        if not re.match(r"^\w+$", username):
            raise ValidationError(
                "Логин должен содержать только буквы, цифры и символы подчеркивания"
            )

        if User.objects.filter(username=username).exists():
            raise ValidationError("Этот логин уже существует")

        return True


class ValidatedDataAPI(APIView):
    """
    View for validated data
    """

    def post(self, request: HttpRequest, *args, **kwargs):
        try:
            ValidatorForRegistration.validate_field(*request.POST.items())
            return Response(
                data={"message": "Данные введенны корректно"},
                status=HTTP_200_OK,
            )
        except ValidationError as e:
            return Response(
                data={
                    "error": str(e),
                },
                status=HTTP_400_BAD_REQUEST,
            )
