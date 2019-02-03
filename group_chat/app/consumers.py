from channels.consumer import AsyncConsumer
from .models import *
import asyncio
from channels.db import database_sync_to_async
import json


class GroupMessageConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({
            "type": "websocket.accept",
        })

    async def websocket_receive(self, event):
        print("receive", event)
        front_text = event.get('text', None)
        if front_text is not None:
            loaded_dict_data = json.loads(front_text)
            msg = loaded_dict_data.get('message')
            print(msg)
            await self.send({
                "type": "websocket.send",
                "text": msg
            })

    async def websocket_disconnect(self, event):
        print("disconnected", event)

