from socket import socket, AF_INET, SOCK_STREAM
from client_connection import ClientConnection
from message import Message
from user_interface import UserInterface
import time
from threading import Thread


class Server(Thread):

    PORT = 11111
    IP = '192.168.178.69'

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

        # Create an INET, STREAMing socket
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        # Bind the socket to a host and port
        self.server_socket.bind((self.IP, self.PORT))
        # Put socket into listening mode (become a server socket)
        self.server_socket.listen(5)
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
        while True:
            print('Search connection...')
            # Accept connection from outside
            client_socket, address = self.server_socket.accept()
            print(client_socket, address)

            # Create a new ClientConnection
            ClientConnection(self, client_socket)

    def on_gamedata(self, client_connection, message):
        """
        This function handels messages containing game-relevant data.
        :param client_connection: client connection of sender
        :type client_connection: ClientConnection
        :param message: message object
        :type message: Message
        :return: None
        """
        for client in self.client_dict:
            if client != client_connection:
                new_msg = Message()
                new_msg.set_type(message.TYPE_GAMEDATA)
                new_msg.set_nickname(message.get_nickname())
                new_msg.set_data(message.get_data())
                new_msg.set_timestamp(int(time.time()*1000))
                client.send_message(new_msg)

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
        :return: 0 or 1
        """
        if not self.client_dict or nickname not in self.client_dict.keys():
            self.client_dict[nickname] = client_connection
            # client_connection.set_nickname(nickname)
            return 1
        else:
            # client_connection.on_error("Nickname is invalid.")
            return 0

    def on_disconnect(self, client_connection):
        """
        This function destroies a client_connection instance and removes the
        conn_dict entry.
        :param client_connection: client connection
        :type client_connection: ClientConnection
        :return: None
        """
        nickname = client_connection.get_nickname()
        self.client_dict.pop(nickname)
        del client_connection
        print("Client '{}' disconnected.").format(nickname)

    def shutdown(self):
        for client_connection in self.client_dict:
            # Send shutdown information to each client
            message = Message()
            message.set_type(message.TYPE_DISCONNECT)
            message.set_nickname("Server")
            message.set_data("Server goes offline")
            message.set_timestamp(int(time.time()*1000))
            client_connection.send_message(message)

            # Close connection to each client
            client_connection.client_socket.close()
            nickname = client_connection.get_nickname()
            del client_connection
            print("Client '{}' disconnected.").format(nickname)

        # NOT CORRECT!!!
        exit()

    def get_client_dict(self):
        return self.client_dict
