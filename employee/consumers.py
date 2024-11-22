# employee/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "notifications"  # Odanın adı
        self.room_group_name = f"notification_{self.room_name}"

        # WebSocket bağlantısını kabul et
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # WebSocket bağlantısını kapatma
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Mesaj alındığında yapılacak işlem
        data = json.loads(text_data)
        message = data['message']

        # Mesajı tüm odaya gönder
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        # Oda içindeki tüm bağlantılara mesaj gönder
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
