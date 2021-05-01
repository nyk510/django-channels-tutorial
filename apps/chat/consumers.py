import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    """message送信出来るようにした consumer"""

    def connect(self):
        print('connect')
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # room への参加 (join)

        #  `WebsocketConsumer` は同期的.
        # すべての channel layer の method は非同期的であるので `async_to_sync` によって同期的に変更する必要がある
        async_to_sync(self.channel_layer.group_add)(
            # Group names are restricted to ASCII alphanumerics, hyphens, and periods only. 
            self.room_group_name,
            self.channel_name
        )

        # accept されないと、接続が拒否されて closed になる.
        # フロントでは `Connection closed before receiving a handshake response` となる
        # [example] 例えばユーザの承認が出来ない場合などには accept を行わない
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        print('disconnect channel')
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data: str):
        """front javascript からテキストデータが送信された時の動作
        """
        print('recieve message')
        # text_data は string なので json.loads で dict へ変換する
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # room group に対してメッセージを送信
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            # 送信する内容の object. 
            # chat_message の event 引数に渡される
            {
                # type: handler の名前. 
                # この class の instalce method 名と一致する必要がある (詳しくは `group_send` を見る)
                'type': 'chat_message_2',
                'message': message,
                # いろいろと情報を付随しておくれる
                'foo': dict()
            }
        )

    # Receive message from room group
    def chat_message_2(self, event):
        print(event, 'chat_message')
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))


class AsyncChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
