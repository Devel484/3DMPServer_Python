from utils.message import Message
import json


class LobbyClient(object):

    def __init__(self, client):
        self.client = client    # client_connection
        self.ready = False

    def is_ready(self):
        return self.ready

    def set_ready(self, ready):
        self.ready = ready

    def get_client(self):
        return self.client


class Lobby(object):

    MINIMUM_PLAYERS = 2
    START_TIMER = 5

    def __init__(self, server, party):
        self.server = server
        self.clients = {}
        self.party = party

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
                self.send_lobby_init(client)
            else:
                return

        lobby_client = self.clients[client.get_nickname()]

        if "ready" in data.keys():
            lobby_client.set_ready(data["ready"])

        if "join" in data.keys() and not data["join"]:
            self.remove(client)

        self.send_lobby_status()

    def send_lobby_init(self, client):
        lobby_settings = {"start_timer": Lobby.START_TIMER, "minimum_players": Lobby.MINIMUM_PLAYERS}

        message = Message()
        message.set_data(lobby_settings)
        message.set_type(Message.TYPE_LOBBYDATA)
        client.send_message(message)

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

        if all_ready and len(self.clients) >= Lobby.MINIMUM_PLAYERS:
            status["start"] = True

            party_dict = dict()
            for lobby_client in self.clients.values():
                client = lobby_client.get_client()
                party_dict[client.get_nickname()] = client

            self.party.set_client_list(party_dict)
            self.server.set_state(self.server.STATE_GAME_INIT)
        else:
            status["start"] = False

        message = Message()
        message.set_data(status)
        message.set_type(Message.TYPE_LOBBYDATA)

        for lobby_client in self.clients.values():
            client = lobby_client.get_client()
            client.send_message(message)
