"""
Service for edit and update user
"""

import logging

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
    def update_and_response(cls, request, instance, serializer):
        """
        Method for update data user
        """
        uploaded_file = request.FILES.get("avatar")
        file_name = cls.file_saving_and_file_name(uploaded_file)
        cls.update_instance(request, serializer, instance, file_name)
        return Response(
            data={
                "message": "Данные обновлены успешно",
            },
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def file_saving_and_file_name(file):
        """
        Method for saving file in MinIO
        """
        file_name = file.name
        minio.upload_to_minio(file_name, file)

        logger.debug("Сохранение в MinIO прошло успешно")
        return file_name

    @staticmethod
    def update_instance(request, serializer, instance, name):
        """
        Updating instance
        """
        request.data["avatar"] = name
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, request.data)
        serializer.save()
        logger.debug("Обновление данных пользователя прошло успешно")
