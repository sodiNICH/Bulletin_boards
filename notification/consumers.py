"""
Consumer for async Websocket
"""

import json
import logging
from channels.generic.websocket import AsyncJsonWebsocketConsumer


logger = logging.getLogger(__name__)


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        logger.debug("коннект к вебсокет")
        if user_id := self.scope["cookies"].get("user_id"):
            self.user_id = user_id
            await self.channel_layer.group_add(
                f"user_notification_{user_id}",
                self.channel_name,
            )
        await self.accept()

    async def disconnect(self, code):
        try:
            if self.user_id is not None:
                await self.channel_layer.group_discard(
                    f"user_notification_{self.user_id}",
                    self.channel_name,
                )
        except AttributeError:
            pass

    async def send_message(self, event):
        message = event["message"]

        await self.send(
            text_data=json.dumps(message),
        )
