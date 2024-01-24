"""
Module for tasks in message queue
"""

import logging

from celery import shared_task
from django.contrib.auth import get_user_model

from config.minio_utils import MinIOFileManager
from .services.file_conversion import bytes_to_in_memory_uploaded_file
from .services.edit_profile import UserProfileEditor


logger = logging.getLogger(__name__)
User = get_user_model()


@shared_task()
def update_profile(data):
    """
    Task for updating profile
    """
    request = data["request"]
    instance_data = data["instance"]
    avatar = request["avatar"]
    request["avatar"] = bytes_to_in_memory_uploaded_file(
        avatar["byte"], avatar["name"], avatar["content_type"]
    )

    edit_user_object = UserProfileEditor(MinIOFileManager, logger)
    edit_user_object.update_profile(request, instance_data)
    logger.debug("Таска сработала")
