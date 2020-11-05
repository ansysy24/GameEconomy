from asgiref.sync import async_to_sync

from channels.generic.websocket import WebsocketConsumer


class BalanceConsumer(WebsocketConsumer):

    def connect(self):
        self.user = self.scope["user"]
        async_to_sync(self.channel_layer.group_add)('render_updates_group', self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)('render_updates_group', self.channel_name)

    def render(self, event):
        if self.user.id == event['id']:
            self.send(text_data=event['data'])

    # Receive message from WebSocket
    def receive(self, text_data):
        pass
