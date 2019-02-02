from channels.generic.websocket import AsyncWebsocketConsumer
from channels.consumer import AsyncConsumer
from .models import *
import asyncio
from channels.db import database_sync_to_async


class GroupMessageConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("connnected", event)

    async def websocket_recieve(self, event):
        print("connnected", event)

    async def websocket_disconnect(self, event):
        print("connnected", event)


#
# class GroupMessageConsumer(AsyncWebsocketConsumer):
#
#     async def connect(self):
#
#         if self.scope["user"].is_anonymous:
#             print("anonymous")
#             await self.close()
#         else:
#             print("accepted")
#             await self.accept()
#
#     async def receive(self, text_data=None, bytes_data=None, **kwargs):
#         print("receiving")
#         await self.send(text_data="receiving")
#
#     async def close(self, code=None):
#         print("closed")
#         await self.close()
