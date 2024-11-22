from channels.generic.websocket import AsyncWebsocketConsumer
import json


class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Приєднання до групи
        await self.channel_layer.group_add(
            'comments',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Відключення від групи
        await self.channel_layer.group_discard(
            'comments',
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        # Логіка обробки повідомлення, якщо потрібно

        # Відправка даних у групу
        await self.channel_layer.group_send(
            'comments',
            {
                'type': 'comment_message',
                'message': data['message']
            }
        )

    async def comment_message(self, event):
        message = event['message']
        # Відправка повідомлення через WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
