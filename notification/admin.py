from django.contrib import admin
from .models import NotificationAdModels


@admin.register(NotificationAdModels)
class NotificationAdmin(admin.ModelAdmin):
    model = NotificationAdModels
    list_display = (
        "seller",
        "advertisement",
    )
