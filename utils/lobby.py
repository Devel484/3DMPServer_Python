from utils.message import Message
import json


class LobbyClient(object):

    def __init__(self, client):
        self.client = client
        self.ready = False

    def is_ready(self):
        return self.ready

    def set_ready(self, ready):
        self.ready = ready

    def get_client(self):
        return self.client


class Lobby(object):

    def __init__(self):
        self.clients = {}

    def add(self, client):
        if client.get_nickname() in self.clients.keys():
            return False
        self.clients[client.get_nickname()] = LobbyClient(client)
        return True

    def remove(self, client):
        if client.get_nickname() not in self.clients.keys():
            return False
        del self.clients[client.get_nickname()]
        return True

    def on_lobbydata(self, message):
        client = message.get_source()
        data = message.get_data()
        if client.get_nickname() not in self.clients.keys():
            if "join" in data.keys() and data["join"]:
                self.add(client)
            else:
                return

        lobby_client = self.clients[client.get_nickname()]

        if "ready" in data.keys():
            lobby_client.set_ready(data["ready"])

        if "join" in data.keys() and not data["join"]:
            self.remove(client)

        self.send_lobby_status()

    def send_lobby_status(self):

        """

        data {
            "0": {},
            "1: {},
            "start": True/False
        }

        :return:
        """

        status = dict()
        all_ready = True
        slot = 0

        for lobby_client in self.clients.values():
            client = lobby_client.get_client()

            client_values = dict()
            client_values["nickname"] = client.get_nickname()
            client_values["ready"] = lobby_client.is_ready()

            if not lobby_client.is_ready():
                all_ready = False

            status[slot] = client_values
            slot += 1

        status["start"] = all_ready

        message = Message()
        message.set_data(status)
        message.set_type(Message.TYPE_LOBBYDATA)

        for lobby_client in self.clients.values():
            client = lobby_client.get_client()
            client.send_message(message)
