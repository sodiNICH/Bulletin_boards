"""
Service for edit and update user
"""

import os
import logging

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile

from rest_framework import status
from rest_framework.response import Response

from minio_utils import MinIOObject


minio = MinIOObject()
logger = logging.getLogger(__name__)


class EditProfile:
    """
    Class with methods for edit user
    """

    @classmethod
    def update(cls, request, instance, serializer):
        """
        Method for update data user
        """
        uploaded_file = request.FILES.get("avatar")
        file_data = cls.file_saving(uploaded_file)
        cls.deleting_file_from_folder(file_data["path"])
        cls.update_instance(request, serializer, instance, file_data["name"])
        return Response(
            data={
                "message": "Данные обновлены успешно",
            },
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def file_saving(file):
        """
        Method for saving file in MinIO
        """
        file_path = f"/{settings.MEDIA_ROOT}/{file}"
        if file and isinstance(file, InMemoryUploadedFile):
            with open(file_path, "wb+") as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            logger.debug("Сохранение файла прошло успешно")

        file_name = file.name
        minio.upload_to_minio(file_path, file_name)

        logger.debug("Сохранение в MinIO прошло успешно")
        data = {
            "path": file_path,
            "name": file_name,
        }
        return data

    @staticmethod
    def deleting_file_from_folder(path):
        """
        Method for deleting file in MinIO
        """
        os.remove(path)

    @staticmethod
    def update_instance(request, serializer, instance, name):
        """
        Updating instance
        """
        request.data["avatar"] = minio.get_minio_object_url(name)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, request.data)
        serializer.save()
        logger.debug("Обновление данных пользователя прошло успешно")
