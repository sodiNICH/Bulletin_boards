"""
Service for functions related to authorization (JWT)
"""

from venv import logger

from django.db.models import QuerySet
from django.http import HttpResponse

from rest_framework_simplejwt.tokens import RefreshToken


class OperationForUserAuth:
    """
    Utility class for authentication-related operations.
    """

    @staticmethod
    def generate_tokens(user):
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
        logger.debug('Токена созданы и добавлены')

    @classmethod
    def delete_cookie(cls, response):
        '''
        Deleting tokens from cookies
        '''
        response.delete_cookie("refresh")
        response.delete_cookie("access")
        response.delete_cookie("user_id")
