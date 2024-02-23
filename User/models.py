"""
Models related User
"""

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    """
    DB USER
    """

    groups = models.ManyToManyField(
        Group,
        related_name="user_group",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="user_permission",
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
    subscriptions = models.ManyToManyField(
        "User.User", blank=True, related_name="subscriptions_to"
    )
    subscribers = models.ManyToManyField(
        "User.User", blank=True, related_name="subscribers_to"
    )
    favorites = models.ManyToManyField(
        "advertisements.Advertisements", blank=True, related_name="Favorites"
    )
    advertisements = models.ManyToManyField(
        "advertisements.Advertisements", blank=True, related_name="Advertisements"
    )
    chats = models.ManyToManyField("chat.Chat", blank=True)

    def __str__(self) -> str:
        return f"{self.pk} {self.username}"

    class Meta:
        ordering = ("created_at",)
        verbose_name = "пользователя"
        verbose_name_plural = "Пользователи"
