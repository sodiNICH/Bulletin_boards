"""
Utility configurations for MinIO
"""

import os
import logging
from datetime import timedelta
from django.conf import settings

from minio import Minio

logger = logging.getLogger(__name__)


class MinIOObject:
    """
    Basic operations with MinIo
    """

    @staticmethod
    def get_minio_client():
        """
        Client minio output
        """
        return Minio(
            endpoint=settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=False,
        )

    def upload_to_minio(self, file_path, object_name):
        """
        Uploading file to minio
        """
        minio_client = self.get_minio_client()
        file_size = os.path.getsize(file_path)
        print("Клиент minio подключен")
        with open(file_path, "rb") as file_data:
            minio_client.put_object(
                bucket_name=settings.MINIO_BUCKET_NAME,
                object_name=object_name,
                data=file_data,
                length=file_size,
            )

    def get_minio_object_url(self, object_name):
        """
        Creating url for file
        """
        minio_client = self.get_minio_client()
        minio_file_url = minio_client.presigned_get_object(
            bucket_name=settings.MINIO_BUCKET_NAME,
            object_name=object_name,
            expires=timedelta(
                seconds=3600
            ),  # Время жизни URL в секундах (в данном случае, 1 час)
        )
        logger.info(minio_file_url)
        return minio_file_url
