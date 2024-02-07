from celery import shared_task
from django.contrib.auth import get_user_model

from config.minio_utils import MinIOFileManager
from services.file_conversion import bytes_to_in_memory_uploaded_file
from .models import Advertisements


User = get_user_model()


@shared_task
def create_ad_task(data):
    paths_img = upload_images(data.get("images"))
    data["images"] = paths_img

    user_id = data["owner"]
    data["owner"] = User.objects.get(pk=user_id)

    ad = Advertisements.objects.create(**data)
    data["owner"].advertisements.add(ad)

    print("Таска сработала")


def upload_images(images_data):
    paths_img = []
    for image_data in images_data:
        image = bytes_to_in_memory_uploaded_file(
            file_data=image_data[0], file_name=image_data[1], content_type="image/jpeg"
        )
        MinIOFileManager.upload_to_minio(file_obj=image, file_name=image.name)
        paths_img.append(f"/media/{image.name}/")
    return paths_img
