"""
Service for functions related to authorization (JWT)
"""

from venv import logger

from django.db.models import QuerySet
from django.http import HttpResponse
from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser

from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from User.serializers import UserSerializer


User = get_user_model()


class OperationForUser:
    """
    Utility class for authentication-related operations.
    """

    @staticmethod
    def generate_tokens(user: QuerySet) -> dict:
        """
        Generate refresh and access tokens for the given user
        """
        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)

        return {
            "refresh": refresh_token,
            "access": access_token,
        }

    @classmethod
    def set_cookies(cls, user: QuerySet, response: HttpResponse):
        """
        Adding tokens to the response cookie
        """
        tokens = cls.generate_tokens(user)
        # Adding tokens to cookies
        response.set_cookie(
            "refresh", str(tokens["refresh"]), httponly=True, samesite="Strict"
        )
        response.set_cookie(
            "access", tokens["access"], httponly=True, samesite="Strict"
        )
        logger.debug("Токена созданы и добавлены")

    @staticmethod
    def delete_cookie(response: HttpResponse):
        """
        Deleting tokens from cookies
        """
        response.delete_cookie("refresh")
        response.delete_cookie("access")
        response.delete_cookie("user_id")

    @staticmethod
    def caching_user(pk, request) -> Response | None:
        """
        Checking user for caching
        """
        user_cache_key = f"user_{pk}"

        if cached_user := cache.get(user_cache_key):
            serializer = UserSerializer(cached_user, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        cached_user: AbstractBaseUser = User.objects.get(pk=pk)
        timeout = 600 if request.user.id == pk else 300
        cache.set(user_cache_key, cached_user, timeout=timeout)
        return None
