"""
Module for tasks in message queue
"""

import logging

from celery import shared_task
from django.contrib.auth import get_user_model

from config.minio_utils import MinIOFileManager
from services.file_conversion import bytes_to_in_memory_uploaded_file
from .services.update_profile import UserProfileUpdate


logger = logging.getLogger(__name__)
User = get_user_model()


@shared_task()
def update_profile(request_data, user_id):
    """
    Task for updating profile
    """
    interface_for_update = prepare_data(request_data)
    update_user_profile(request_data, interface_for_update, user_id)
    logger.debug("Таска сработала")


def prepare_data(request_data):
    """
    Preparing data for profile update
    """
    if avatar := request_data.get("avatar"):
        request_data["avatar"] = bytes_to_in_memory_uploaded_file(
            avatar["byte"], avatar["name"], avatar["content_type"]
        )
        interface_for_update = UserProfileUpdate(logger, MinIOFileManager)
    else:
        interface_for_update = UserProfileUpdate(logger)

    return interface_for_update


def update_user_profile(request_data, interface_for_update, user_id):
    """
    Updating a user profile
    """
    instance = User.objects.get(pk=user_id)
    instance_data = {
        "avatar": instance.avatar,
        "pk": instance.pk,
    }
    interface_for_update.update_profile(request_data, instance_data)
