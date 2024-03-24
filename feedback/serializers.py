import logging
from rest_framework import serializers

from .models import Feedback
from config.minio_utils import MinIOFileManager


logger = logging.getLogger(__name__)


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"

    def to_internal_value(self, data):
        images = data.getlist("images")
        user = data.get("owner")

        if images:
            images_urls = []
            for image in images:
                logger.debug(image)
                file_name = f"{user}-{image.name}"
                MinIOFileManager.upload_to_minio(image, f"{user}-{image.name}")
                images_urls.append(f"/media/{file_name}/")
            data.setlist("images", images_urls)
        return super().to_internal_value(data)
