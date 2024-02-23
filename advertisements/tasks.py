from typing import Any
from celery import shared_task
from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from django.core.files.uploadedfile import InMemoryUploadedFile

from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync

from config.minio_utils import MinIOFileManager
from services.file_conversion import bytes_to_in_memory_uploaded_file
from .models import Advertisements
from notification.models import NotificationAdModels


User = get_user_model()


@shared_task
def create_ad_task(data):
    paths_img: list = upload_images(data.get("images"))
    data["images"] = paths_img

    user_id: int = data["owner"]
    data["owner"] = User.objects.get(pk=user_id)

    ad: Advertisements = Advertisements.objects.create(**data)
    data["owner"].advertisements.add(ad)

    seller = data["owner"]
    sending_notification(seller=seller, ad=ad)

    print("Таска сработала")


def sending_notification(seller, ad):
    NotificationAdModels.objects.create(advertisement=ad, seller=seller)
    ad_data: dict[str, Any] = model_to_dict(ad)
    for sub in seller.subscribers.all():
        channel_layer = get_channel_layer()
        name_group = f"user_{sub.id}"
        async_to_sync(channel_layer.group_send)(
            name_group,
            {
                "type": "send_message",
                "message": ad_data,
            },
        )


def upload_images(images_data: list[bytes]) -> list[str]:
    paths_img = []
    for image_data in images_data:
        image: InMemoryUploadedFile = bytes_to_in_memory_uploaded_file(
            file_data=image_data[0], file_name=image_data[1], content_type="image/jpeg"
        )
        MinIOFileManager.upload_to_minio(file_obj=image, file_name=image.name)
        paths_img.append(f"/media/{image.name}/")
    return paths_img
