import socket
import sys
from threading import Thread


class Server(Thread):

    def __init__(self):
        # Start seperate Thread for wait_for_connection
        Thread.__init__(self)
        self.port = 11111
        self.ip = 'localhost'
        self.serversocket = None

        # Create an INET, STREAMing socket
        self.serversocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to a host and port
        self.serversocket.bind((self.ip, self.port))
        # Become a server socket
        self.serversocket.listen(5)

    def run(self):
        self.wait_for_connection()

    def wait_for_connection(self):
        while 1:
            # Accept connection from outside
            (clientsocket, address) = self.serversocket.accept()
            with clientsocket:
                print('Connected by ', address)
                while True:
                    data = clientsocket.recv(1024)
                    if not data:
                        break

    def on_gamedata(self, client_connection):
        pass

    def send_gamedata(self):
        pass
