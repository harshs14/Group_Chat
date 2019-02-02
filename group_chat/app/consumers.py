from channels.generic.websocket import AsyncWebsocketConsumer
from channels.consumer import AsyncConsumer
from .models import *
import asyncio
from channels.db import database_sync_to_async


class GroupMessageConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({
            "type": "websocket.accept",
        })

    async def websocket_recieve(self, event):
        print("receive", event)

    async def websocket_disconnect(self, event):
        print("disconnected", event)

