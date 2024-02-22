from django.db import models


class NotificationAdModels(models.Model):
    """
    Model for publication notifications ad
    """
    seller = models.ForeignKey(
        "User.User",
        on_delete=models.CASCADE,
        blank=False
    )
    advertisement = models.ForeignKey(
        "advertisements.Advertisements",
        on_delete=models.CASCADE,
        blank=False,
    )
