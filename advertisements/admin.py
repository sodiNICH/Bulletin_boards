from django.contrib import admin

from .models import Advertisements


@admin.register(Advertisements)
class AdAdmin(admin.ModelAdmin):
    """
    Admin panel for advertisements
    """
    model = Advertisements
    list_display = (
        "id",
        "created_at",
        "title",
        "images",
    )
