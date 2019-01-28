from channels.generic.websocket import AsyncJsonWebsocketConsumer


class GroupMessageConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):

        if self.scope["user"].is_anonymous:
            print("anonymous")
            await self.close()
        else:
            print("accepted")
            await self.accept()

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        print("receiving")
        await self.send(text_data="receiving")

    async def close(self, code=None):
        print("closed")
        await self.close()
