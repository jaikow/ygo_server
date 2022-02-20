import json
from geventwebsocket import WebSocketApplication


class GameStateApplication(WebSocketApplication):
    ''' Websockets controller defining game-related behavior, interfacing with the Unity UI '''
    ''' Note that this server design heavily implies that the requests are stateful, but that's way more practical for this usage '''
    def on_open(self):
        print("Some client connected!")

    def on_message(self, message):
        if message is None:
            return
        message = json.loads(message)

        if message['msg_type'] == 'message':
            self.broadcast(message)
        elif message['msg_type'] == 'update_clients':
            self.send_client_list(message)

    def send_client_list(self, message):
        current_client = self.ws.handler.active_client
        current_client.nickname = message['nickname']

        self.ws.send(json.dumps({
            'msg_type': 'update_clients',
            'clients': [
                getattr(client, 'nickname', 'anonymous')
                for client in self.ws.handler.server.clients.values()
            ]
        }))

    def broadcast(self, message):
        for client in self.ws.handler.server.clients.values():
            client.ws.send(json.dumps({
                'msg_type': 'message',
                'nickname': message['nickname'],
                'message': message['message']
            }))

    def on_close(self, reason):
        print("Connection closed!")