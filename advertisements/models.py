"""
Model for advertisements
"""

from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField


User = get_user_model()


class Advertisements(models.Model):
    """
    DB AD
    """

    title = models.CharField(
        max_length=255,
        verbose_name="Title",
        null=False,
    )
    condition = models.CharField(
        null=True,
    )
    description = models.TextField(
        max_length=5000,
        null=False,
        validators=[
            MinLengthValidator(
                limit_value=50,
                message="Minimum number of characters: 50",
            )
        ],
        verbose_name="description",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1,
        verbose_name="Price",
    )
    barter = models.TextField(
        max_length=1000,
        validators=[
            MinLengthValidator(
                limit_value=50,
                message="Minimum number of characters: 50",
            )
        ],
        default="",
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        related_name="Owner",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data creation"
    )
    location = models.TextField(
        max_length=1000,
        verbose_name="Location",
    )
    category = models.CharField(
        max_length=100,
        verbose_name="Category",
    )
    images = ArrayField(
        models.CharField(
            max_length=500,
            validators=[
                MinLengthValidator(
                    limit_value=1,
                    message="There must be at least one image",
                )
            ],
        ),
        blank=True,
    )
