"""
Module for custom permissions
"""

from rest_framework.permissions import BasePermission, IsAdminUser


class CustomIsAdminUser(IsAdminUser):
    """
    If the user is authorized or is an administrator
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsOwnerOrReadOnly(BasePermission):
    """
    The user can only modify or delete their own objects
    """

    def has_object_permission(self, request, view, obj):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        return obj == request.user
