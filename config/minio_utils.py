"""
Utility configurations for MinIO
"""

from io import BytesIO
import logging

from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.views import View

from minio import Minio
from minio.error import S3Error

logger = logging.getLogger(__name__)


class MinIOFileManager:
    """
    Basic operations with MinIo
    """

    @staticmethod
    def minio_client():
        """
        Client minio output
        """
        return Minio(
            endpoint=settings.MINIO_STORAGE_ENDPOINT,
            access_key=settings.MINIO_STORAGE_ACCESS_KEY,
            secret_key=settings.MINIO_STORAGE_SECRET_KEY,
            secure=False,
        )

    @classmethod
    def upload_to_minio(cls, file_obj, file_name):
        """
        Uploading file to minio
        """
        minio_client = cls.minio_client()
        file_bytes = file_obj.read()
        file_size = len(file_bytes)

        minio_client.put_object(
            bucket_name=settings.MINIO_STORAGE_MEDIA_BUCKET_NAME,
            object_name=file_name,
            data=BytesIO(file_bytes),
            length=file_size,
        )

    @classmethod
    def delete_from_minio(cls, object_name):
        """
        Deleting file from minio
        """
        try:
            minio_client = cls.minio_client()
            minio_client.remove_object(
                settings.MINIO_STORAGE_MEDIA_BUCKET_NAME, object_name
            )
        except (S3Error, ValueError):
            pass

    @classmethod
    def image_output_via_http_response(cls, object_name):
        """
        Output image
        """
        try:
            minio_object = cls._get_object(object_name)
            image_bytes = cls._read_file(minio_object)
            response = cls._response(image_bytes)
            return response
        except S3Error:
            return HttpResponseNotFound()

    @classmethod
    def _get_object(cls, object_name):
        """
        Get MinIO file-object
        """
        minio_client = cls.minio_client()
        minio_object = minio_client.get_object(
            settings.MINIO_STORAGE_MEDIA_BUCKET_NAME, object_name
        )
        return minio_object

    @staticmethod
    def _read_file(minio_object):
        """
        File reading from minio
        """
        image_bytes = minio_object.read()
        return image_bytes

    @staticmethod
    def _response(image_bytes):
        """
        Creating and return response
        """
        response = HttpResponse(image_bytes, content_type="image/jpeg")
        return response


class ImagePreviewFromMinIO(View):
    """
    Endpoint for output image
    """

    def get(self, request, *args, **kwargs):
        object_name = kwargs.get("name")
        try:
            response = MinIOFileManager.image_output_via_http_response(object_name)
            return response
        except FileNotFoundError:
            return HttpResponseNotFound("File not found")
