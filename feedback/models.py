"""
Model for feedback for advertisements
"""


from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinLengthValidator


class Feedback(models.Model):
    class Rating(models.IntegerChoices):
        DREADFUL = 1, "Ужасно"
        BAD = 2, "Плохо"
        MEDIUM = 3, "Средне"
        NORMAL = 4, "Хорошо"
        GREAT = 5, "Отлично"

    user = models.ForeignKey(
        "User.User",
        on_delete=models.CASCADE,
    )
    ad = models.ForeignKey(
        "advertisements.Advertisements",
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        max_length=1000,
        validators=(MinLengthValidator(limit_value=10),),
        null=False,
    )
    images = ArrayField(
        models.TextField(
            max_length=500,
        ),
        blank=True,
        null=True,
    )
    rating = models.IntegerField(
        choices=Rating.choices,
        default=3,
        blank=False,
    )
    date = models.DateTimeField(
        auto_now_add=True,
        null=True,
    )
