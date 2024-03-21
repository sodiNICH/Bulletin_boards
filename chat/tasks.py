import logging

from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()
logger = logging.getLogger(__name__)


@shared_task()
def update_detail_chat_via_websocket(name_group, message_data):
    async_to_sync(channel_layer.group_send)(
        name_group,
        {
            "type": "send_message_chat",
            "message": message_data,
        },
    )


@shared_task()
def update_chat_list_via_websocket(name_group, chat_data):
    async_to_sync(channel_layer.group_send)(
        name_group,
        {
            "type": "send_chat_list",
            "chat": chat_data,
        },
    )

@shared_task()
def delete_chat_message(name_group, chat_id):
    async_to_sync(channel_layer.group_send)(
        name_group,
        {
            "type": "delete_message_chat",
            "message_id": chat_id,
        },
    )