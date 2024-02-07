"""
Service for edit and update user
"""

from logging import Logger
from minio import Minio
from django.contrib.auth import get_user_model
from django.core.cache import cache


User = get_user_model()


class UserProfileUpdate:
    """
    Class with methods for editing user profile
    """

    def __init__(self, logger: Logger, minio_client: Minio=None):
        self.minio_client = minio_client
        self.logger = logger

    def update_profile(self, request, instance):
        """
        Updating profile and get response
        """
        if uploaded_file := request.get("avatar"):
            self._delete_previous_file(instance["avatar"])
            file_name = self._save_file_and_get_name(uploaded_file, instance["pk"])
            self._update_instance(request, instance, file_name)
        else:
            self._update_instance(request, instance)

    def _delete_previous_file(self, file_name):
        """
        Deleting a previous file
        """
        self.minio_client.delete_from_minio(file_name)
        self.logger.info("File delete with MinIO")

    def _save_file_and_get_name(self, file_obj, pk):
        """
        Method for saving file in MinIO and getting the file name
        """
        object_name = f"{pk}-{file_obj.name}"
        self.minio_client.upload_to_minio(file_obj, object_name)
        self.logger.info("File saved in MinIO successfully")
        return file_obj.name

    def _update_instance(self, request, instance, name=None):
        """
        Updating user instance
        """
        query_set = User.objects.filter(pk=instance['pk'])
        if name:
            request["avatar"] = f"/media/{instance['pk']}-{name}/"
        else:
            del request["avatar"]
        query_set.update(**request)
        cache.set(f"user_{instance['pk']}", query_set[0], timeout=600)
