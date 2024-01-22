"""
Models related User
"""

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    '''
        DB USER
    '''
    groups = models.ManyToManyField(
        Group,
        related_name="user_group",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='user_permission',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
    )
    avatar = models.TextField(
        default="",
    )
    description = models.TextField(
        max_length=200,
        default="",
    )

    class Meta:
        ordering = ('created_at', )
        verbose_name = 'пользователя'
        verbose_name_plural = 'Пользователи'
    
