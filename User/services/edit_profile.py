"""
Service for edit and update user
"""

from logging import Logger

from rest_framework import status
from rest_framework.response import Response

from minio import Minio


class UserProfileEditor:
    """
    Class with methods for editing user profile
    """

    def __init__(self, minio_client: Minio, logger: Logger):
        self.minio_client = minio_client
        self.logger = logger

    def update_profile_and_get_response(self, request, instance, serializer):
        """
        Updating profile and get response
        """
        uploaded_file = request.FILES.get("avatar")
        self._delete_previous_file(instance.avatar)
        file_name = self._save_file_and_get_name(uploaded_file, instance.pk)
        self._update_instance(request, serializer, instance, file_name)
        return self._success_response()

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

    def _update_instance(self, request, serializer, instance, name):
        """
        Updating user instance
        """
        request.data["avatar"] = f"/media/{instance.pk}-{name}/"
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, request.data)
        serializer.save()
        self.logger.info("User data updated successfully")

    def _success_response(self):
        """
        Return a success response
        """
        return Response(
            data={
                "message": "User data updated successfully",
            },
            status=status.HTTP_200_OK,
        )
