import logging
import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer


logger = logging.getLogger(__name__)


class ChatMessageConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        logger.debug("sdjadfbhdsufvghsdfvghsd")
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

    async def receive_json(self, content, **kwargs):
        logger.debug(content)
        if typing_status := content.get("typing"):
            await self.channel_layer.group_send(
                f"chat_{self.chat_id}",
                {
                    "type": "typing_status",
                    "typing": typing_status,
                    "user_id": content.get("user_id"),
                },
            )
        return super().receive_json(content, **kwargs)

    async def typing_status(self, event):
        typing_status = event["typing"]
        user_id = event["user_id"]
        data = {
            "typing": typing_status,
            "user_id": user_id,
        }
        await self.send(
            text_data=json.dumps(data),
        )

    async def delete_message_chat(self, event):
        data = {"delete_message": {"id": event.get("message_id")}}
        await self.send(text_data=json.dumps(data))

    async def send_message_chat(self, event):
        message = event["message"]
        data = {"message": message}

        await self.send(
            text_data=json.dumps(data),
        )

class ChatListConsumers(AsyncJsonWebsocketConsumer):
    async def connect(self):
        logger.debug("sdjadfbhdsufvghsdfvghsd")
        if user_id := self.scope["cookies"].get("user_id"):
            self.user_id = user_id
            await self.channel_layer.group_add(
                f"chat_list_{user_id}",
                self.channel_name,
            )
        return await self.accept()

    async def send_chat_list(self, event):
        chat_data = event["chat"]

        await self.send(
            text_data=json.dumps(chat_data),
        )
