"""
Validations for the chat model
"""

from typing import Any

from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser

from advertisements.models import Advertisements
from .models import Chat


def validate_for_create_chat(attrs: dict[Any], user: AbstractBaseUser) -> None:
    """
    Validation when creating a chat room
    """
    companions = attrs.get("companions", [])
    advert_id = attrs.get("advertisement")
    existing_chat = Chat.objects.filter(companions__in=companions).distinct()
    existing_advert = Chat.objects.filter(advertisement_id=advert_id).exists()

    if existing_chat.exists() and existing_advert:
        raise ValidationError("Chat with these companions already exists.")

    if user not in companions:
        raise ValidationError("You can't create a chat room for unauthorized people")

    companions.remove(user)
    advert: Advertisements | None = attrs.get("advertisement")
    if advert not in companions[0].advertisements.all():
        raise ValidationError(f"None of the users owns the ad - {advert}")
    companions.append(user)
