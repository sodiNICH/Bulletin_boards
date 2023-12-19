"""
Custom forms for User admin
"""

from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
)
from django.contrib.auth import get_user_model


User = get_user_model()


class CustomCreationForm(UserCreationForm):
    """
    Form for the admin area
    """

    class Meta:
        model = User
        fields = (
            "username",
            "password",
        )


class CustomChangeForm(UserChangeForm):
    """
    Form for the admin area
    """

    class Meta:
        model = User
        fields = (
            "username",
            "password",
        )
