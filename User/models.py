"""
Models related User
"""

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.urls import reverse

from autoslug import AutoSlugField


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
    slug = AutoSlugField(
        unique=True,
        editable=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        self.slug = f'{self.username.lower().replace(" ", "-")}-{self.pk}'
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("user", kwargs={"slug": self.slug})

    def __str__(self):
        return self.slug

    class Meta:
        ordering = ('created_at', )
        verbose_name = 'пользователя'
        verbose_name_plural = 'Пользователи'
    
