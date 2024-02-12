from cgitb import text
import json
import logging
import redis
from jwt import decode
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer


logger = logging.getLogger(__name__)


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        logger.debug(self.scope)
        try:
            if user_id := self.scope["cookies"].get("user_id"):
                self.user_id = user_id
                await self.channel_layer.group_add(
                    f"user_{user_id}",
                    self.channel_name,
                )
        except KeyError:
            pass
        finally:
            await self.accept()

    async def disconnect(self, code):
        try:
            if self.user_id is not None:
                await self.channel_layer.group_discard(
                    f"user_{self.user_id}",
                    self.channel_name,
                )
        except AttributeError:
            pass

    async def send_message(self, event):
        message = event["message"]

        await self.send(
            text_data=json.dumps(message),
        )
