import socket


class MPSocket(socket.socket):

    BUFFER_SIZE = 4096

    def __init__(self, **kwargs):
        socket.socket.__init__(self, **kwargs)

    def receive(self):
        received_data = b''
        while True:
            piece = self.recv(MPSocket.BUFFER_SIZE)
            received_data += piece
            if len(piece) < MPSocket.BUFFER_SIZE:
                return received_data

