from threading import Thread
from utils.message import Message
import time


class PartyClient(object):

    def __init__(self, client):
        self.client = client    # client_connection
        self.ready = False

    def set_ready(self, ready):
        self.ready = ready

    def get_ready(self):
        return self.ready

    def get_client(self):
        return self.client


class Party(object):

    START_TIMER = 5

    def __init__(self, server):
        self.server = server
        self.clients = {}   # Dict {nickname, PartyClient}

    def set_client_list(self, clients):
        # lobby_clients: Dict{nickname, client_connection}
        for client in clients.values():
            self.clients[client.get_nickname()] = PartyClient(client)

    def on_gamedata(self, message):
        nickname = message.get_source().get_nickname()
        data = message.get_data()
        state = self.server.get_state()
        all_ready = True

        if state == self.server.STATE_GAME_INIT:
            if "ready" in data.keys() and data["ready"]:
                # Client is ready to play
                self.clients.get(nickname).set_ready(True)

            for client in self.clients.values():
                if not client.get_ready():
                    all_ready = False

            if all_ready:
                self.start_game()

        elif state == self.server.STATE_GAME:
            # Send message from client to all other clients
            for party_client in self.clients.values():
                client = party_client.get_client()
                if client.get_nickname() != nickname:
                    client.send_message(message)

    def start_game(self):
        self.server.set_state(self.server.STATE_GAME)
        # Send start message
        status = {"start": True}
        message = Message()
        message.set_type(Message.TYPE_GAMEDATA)
        message.set_data(status)

        for party_client in self.clients.values():
            client = party_client.get_client()
            client.send_message(message)
