import logging
import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer


logger = logging.getLogger(__name__)


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        if chat_id := self.scope["url_route"]["kwargs"].get("chat_id"):
            self.chat_id = chat_id
            await self.channel_layer.group_add(
                f"chat_{chat_id}",
                self.channel_name,
            )
        return await self.accept()

    async def disconnect(self, code):
        try:
            if self.chat_id is not None:
                await self.channel_layer.group_discard(
                    f"chat_{self.chat_id}",
                    self.channel_name,
                )
        except AttributeError:
            pass

    async def send_message_chat(self, event):
        message = event["message"]

        await self.send(
            text_data=json.dumps(message),
        )
