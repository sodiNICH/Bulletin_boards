from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.postgres.fields import ArrayField


class Chat(models.Model):
    companions = models.ManyToManyField(
        "User.User",
        blank=False,
    )
    advertisement = models.ForeignKey(
        "advertisements.Advertisements", on_delete=models.CASCADE
    )
    messages = models.ManyToManyField(
        "chat.Message", blank=True, related_name="chat_messages"
    )


class Message(models.Model):
    chat = models.ForeignKey(
        "chat.Chat",
        on_delete=models.CASCADE,
        null=False,
        default="",
        related_name="chat_messages",
    )
    text = models.TextField(
        max_length=200, validators=[MinLengthValidator(limit_value=1)], blank=False
    )
    images = ArrayField(
        models.TextField(
            max_length=500,
        ),
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Chat message creation"
    )
    owner = models.ForeignKey("User.User", on_delete=models.CASCADE, null=False)
