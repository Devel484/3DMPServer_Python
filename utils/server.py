from socket import socket, AF_INET, SOCK_STREAM, timeout
from utils.client_connection import ClientConnection
from utils.message import Message
from utils.user_interface import UserInterface
from utils.lobby import Lobby
from utils.party import Party
import time
from threading import Thread


class Server(Thread):

    # IMPORTANT !!
    STATE_IDLE = 'idle'
    STATE_LOBBY = 'lobby'
    STATE_GAME_INIT = 'game_init'
    STATE_GAME = 'game'

    PORT = 11111
    IP = '127.0.0.1'
    EXIT = False
    CLIENT_TIMEOUT = 10 * 1000

    FILTER_MESSAGES = []

    def __init__(self):
        """
        Creates a instance of Server and creates a server_socket.
        :return: None
        """

        # Start a second Thread for wait_for_connection
        Thread.__init__(self)
        # Create User Interface
        UserInterface(self)

        # Dict containing all connections with nicknames
        self.client_dict = dict()

        self.state = Server.STATE_IDLE

        # Create an INET, STREAMing socket
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        # Bind the socket to a host and port
        self.server_socket.bind((self.IP, self.PORT))

        self.party = Party(self)
        self.lobby = Lobby(self, self.party)
        print("Socket successfully created.")

    def run(self):
        """
        This functions starts wait_for_connection.
        :return: None
        """
        self.wait_for_connection()

    def wait_for_connection(self):
        """
        This function starts a loop which checks if a new client connects to the server.
        :return: None
        """
        print('Search connection...')
        while not Server.EXIT:
            try:
                self.server_socket.settimeout(0.5)
                # Put socket into listening mode (become a server socket)
                self.server_socket.listen(5)
                # Accept connection from outside
                client_socket, address = self.server_socket.accept()
                print(client_socket, address)
            except timeout:
                pass
            else:
                # Create a new ClientConnection
                ClientConnection(self, client_socket)

    def on_gamedata(self, message):
        """
        This function handels messages containing game-relevant data.
        :param message: message object
        :type message: Message
        :return: None
        """
        self.party.on_gamedata(message)

    def send_gamedata(self):
        """
        Send game-relevant data.
        :return: None
        """
        pass

    def on_connect(self, client_connection, nickname):
        """
        This function adds the nickname of a client to the conn_dict dictionary,
        if the nickname is valid. Otherwise return error state.
        :param client_connection: client connection
        :type client_connection: ClientConnection
        :param nickname: nickname of client
        :type nickname: str
        :return: bool
        """
        if not self.client_dict or nickname not in self.client_dict.keys():
            self.client_dict[nickname] = client_connection
            # client_connection.set_nickname(nickname)
            return True
            # client_connection.on_error("Nickname is invalid.")
        return False

    def on_disconnect(self, client_connection, reason):
        """
        This function destroies a client_connection instance and removes the
        conn_dict entry.
        :param client_connection: client connection
        :type client_connection: ClientConnection
        :param reason: Reason for disconnecting
        :type reason: String
        :return: None
        """
        # Don't send a message to the client if he disconnected
        if reason != "client":
            message = Message()
            message.set_type(message.TYPE_DISCONNECT)
            message.set_data({"reason": reason})
            client_connection.send_message(message)

        nickname = client_connection.get_nickname()
        if nickname in self.client_dict:
            self.client_dict.pop(nickname)
        client_connection.stop = True
        client_connection.client_socket.close()

        self.lobby.remove(client_connection)

        del client_connection
        print("Client '%s' disconnected." % nickname)

    def on_lobbydata(self, message):
        self.lobby.on_lobbydata(message)

    def shutdown(self):
        for client_connection in self.client_dict.values():
            # Send shutdown information to each client
            message = Message()
            message.set_type(message.TYPE_DISCONNECT)
            message.set_data({"reason": "server goes offline"})
            client_connection.send_message(message)

        Server.EXIT = True
        time.sleep(0.2)

        for client_connection in self.client_dict.values():
            # Close connection to each client
            client_connection.client_socket.close()
            nickname = client_connection.get_nickname()
            del client_connection
            print("Client '%s' disconnected." % nickname)

    def get_client_dict(self):
        return self.client_dict

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

