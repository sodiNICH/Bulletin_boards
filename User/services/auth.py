"""
Service for functions related to authorization (JWT)
"""

from venv import logger

from django.db.models import QuerySet
from django.http import HttpResponse

from rest_framework_simplejwt.tokens import RefreshToken


class AuthUser:
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

    def set_cookies(self, user: QuerySet, response: HttpResponse):
        """
        Adding tokens to the response cookie
        """
        tokens = self.generate_tokens(user)
        response.set_cookie(
            "refresh", str(tokens["refresh"]), httponly=True, samesite="Strict"
        )
        response.set_cookie(
            "access", tokens["access"], httponly=True, samesite="Strict"
        )
        logger.debug('Токена созданы')

    def delete_cookie(self, response):
        '''
        Deleting tokens from cookies
        '''
        response.delete_cookie("refresh")
        response.delete_cookie("access")
