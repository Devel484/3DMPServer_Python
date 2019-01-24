from message import Message
from threading import Thread
import time


class ClientConnection(Thread):

    # message   : Class message
    # msg       : Received Data

    def __init__(self, server, client_socket):
        Thread.__init__(self)
        self.server = server
        self.client_socket = client_socket
        self.start()

    def send_message(self, message):
        self.client_socket.sendall(bytes((str(message)+'\0').encode("utf-8")))

    def on_message(self, msg):
        message = Message(msg)
        print(message)
        msg_type = message.get_type()

        # Check for msg_type
        if msg_type == message.TYPE_PING:
            self.on_ping()
        elif msg_type == message.TYPE_DISCONNECT:
            self.on_disconnect()
        elif msg_type == message.TYPE_TIMEOUT:
            self.on_timeout()
        elif msg_type == message.TYPE_GAMEDATA:
            self.on_gamedata()

    def on_ping(self):
        # Create and send pong message
        message = Message()
        message.set_type(message.TYPE_PING)
        message.set_timestamp(int(time.time()*1000))
        message.set_data({"pong": True})
        self.send_message(message)

    def on_disconnect(self):
        # Close connection
        self.client_socket.close()
        self.server.on_disconnect(self)

    def on_timeout(self):
        pass

    def on_gamedata(self):
        pass

    def on_error(self):
        pass

    def run(self):
        received_data = ""
        while True:
            piece = str(self.client_socket.recv(4096).decode("utf-8"))
            if piece == '':
                continue
            find = piece.find('\0')
            while find != -1:
                received_data += piece[:find]
                self.on_message(received_data)
                received_data = ""
                piece = piece[find+1:]
                find = piece.find("\0")
            else:
                received_data += piece
