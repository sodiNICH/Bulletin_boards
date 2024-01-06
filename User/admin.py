"""
Admin panel for user model
"""

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomChangeForm, CustomCreationForm


User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin panel for user
    """

    add_form = CustomCreationForm
    form = CustomChangeForm
    model = User
    list_display = (
        "id",
        "avatar",
        "username",
        "password",
    )
