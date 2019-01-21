from message import Message
from threading import Thread


class ClientConnection(Thread):

    def __init__(self, client_socket):
        Thread.__init__(self)
        self.client_socket = client_socket
        self.start()

    def send_message(self, message):
        self.client_socket.sendall(bytes((str(message)+'\0').encode("utf-8")))

    def on_message(self, message):
        message = Message(message)
        print(message)

    def on_ping(self):
        pass

    def on_disconnect(self):
        pass

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
