"""
Module with custom middleware related User
"""

import logging
from math import trunc
from typing import Any

from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse_lazy

from jwt import decode
from jwt.exceptions import DecodeError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from rest_framework import status

# from asgiref.sync import sync_to_async


User = get_user_model()
logger = logging.getLogger(__name__)


class TokenAuthMiddleware:
    """
    Middleware for token verification and update
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        access_token = request.COOKIES.get("access")

        if access_token:
            logger.info("Tokens exist")
            if not self.check_token_validity(access_token):
                logger.info("Token is no longer needed")
                return self.delete_tokens(request)

            if self.token_expired(access_token):
                logger.info("Token has expired")
                return self.update_tokens_and_response(request)

            request.META["HTTP_AUTHORIZATION"] = f"Token {access_token}"
            logger.info("Token added to the header")
        else:
            logger.info("Tokens auth not found")
        return self.get_response(request)

    @staticmethod
    def check_token_validity(access_token) -> bool:
        """
        Checking for the presence of a user in DB
        """
        user_id = decode(access_token, options={"verify_signature": False}).get('user_id')
        return User.objects.filter(id=user_id).exists()

    @staticmethod
    def token_expired(access_token) -> bool:
        """
        Checking token lifetime
        """
        try:
            expiration_time = decode(access_token, options={"verify_signature": False})["exp"]
            remaining_time = expiration_time - timezone.now().timestamp()
            logger.info("Token validity period - %s", trunc(remaining_time))
            return trunc(remaining_time) <= 10
        except (DecodeError, KeyError):
            return False

    @staticmethod
    def tokens_updates(refresh_token) -> dict:
        """
        Update token
        """
        user_id = decode(refresh_token, options={"verify_signature": False}).get('user_id')
        user = User.objects.get(id=user_id)
        new_access_token = AccessToken.for_user(user)
        new_refresh_token = RefreshToken.for_user(user)
        logger.info("Tokens updates")
        return {"access": new_access_token, "refresh": new_refresh_token}

    def delete_tokens(self, request):
        """
        Delete tokens and return the response
        """
        response = self.get_response(request)
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        logger.info("Tokens delete")
        return response

    def update_tokens_and_response(self, request):
        """
        Update tokens and return the response
        """
        refresh_token = request.COOKIES["refresh"]
        new_tokens = self.tokens_updates(refresh_token)

        request.META["HTTP_AUTHORIZATION"] = f'Token {new_tokens["access"]}'
        response = self.get_response(request)
        response.set_cookie("access", new_tokens["access"], httponly=True, samesite="Strict")
        response.set_cookie("refresh", new_tokens["refresh"], httponly=True, samesite="Strict")

        return response


class CheckCookiesMiddleware:
    """
    Middleware for cheking cookies
    """
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> Any:
        response = self.get_response(request)
        if access_token := request.COOKIES.get("access"):
            self.check_user_id(request, access_token, response)
        else:
            response.set_cookie("user_id")
        return response

    def check_user_id(self, request ,access_token, response):
        """
        Check user id in cookies
        """
        if not request.COOKIES.get("user_id"):
            user_id = decode(access_token, options={"verify_signature": False}).get('user_id')
            response.set_cookie("user_id", user_id)


class RedirectMiddleware:
    """
    Custom redirect middleware
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.auth_check(request)

    def auth_check(self, request):
        """
        Function with
        """
        response = self.get_response(request)
        if (
            response.status_code == status.HTTP_401_UNAUTHORIZED
            and not request.user.is_authenticated
        ):
            return HttpResponseRedirect(reverse_lazy("login-template"))
        return response
