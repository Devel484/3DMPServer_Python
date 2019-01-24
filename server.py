from socket import socket, AF_INET, SOCK_STREAM
from client_connection import ClientConnection
import sys
from threading import Thread


class Server(Thread):

    PORT = 11111
    IP = '192.168.137.154'

    def __init__(self):
        # Start a second Thread for wait_for_connection
        Thread.__init__(self)

        # Dict containing all connections with nicknames
        self.conn_dict = dict()

        # Create an INET, STREAMing socket
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        # Bind the socket to a host and port
        self.server_socket.bind((self.IP, self.PORT))
        # Put socket into listening mode (become a server socket)
        self.server_socket.listen(5)
        print("Socket successfully created.")

    def run(self):
        self.wait_for_connection()

    def wait_for_connection(self):
        while True:
            print('Search connection...')
            # Accept connection from outside
            client_socket, address = self.server_socket.accept()
            print(client_socket, address)

            # Create a new ClientConnection
            ClientConnection(self, client_socket)

    def on_gamedata(self, client_connection):
        pass

    def send_gamedata(self):
        pass

    def on_connect(self, client_connection, nickname):
        if not self.conn_dict or nickname not in self.conn_dict.values():
            self.conn_dict[client_connection] = nickname
            client_connection.set_nickname(nickname)
            # return 1
        else:
            client_connection.on_error("Nickname is invalid.")
            # return 0

    def on_disconnect(self, client_connection):
        self.conn_dict.pop(client_connection)
        del client_connection
        print("Client disconnected.")
