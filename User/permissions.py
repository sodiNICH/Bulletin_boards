"""
Module for custom permissions
"""

import logging
from rest_framework.permissions import BasePermission, IsAdminUser

from django.http import HttpRequest

logger = logging.getLogger(__name__)


class CustomIsAdminUser(IsAdminUser):
    """
    If the user is authorized or is an administrator
    """

    def has_permission(self, request: HttpRequest, view):
        return request.user and request.user.is_staff


class IsOwnerOrReadOnly(BasePermission):
    """
    The user can only modify or delete their own objects
    """

    def has_object_permission(self, request: HttpRequest, view, obj):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        return obj == request.user
