import socket


class MPSocket(socket.socket):

    BUFFER_SIZE = 4096

    def receive(self):
        received_data = b''
        while True:
            piece = self.recv(MPSocket.BUFFER_SIZE)
            received_data += piece
            if len(piece) < MPSocket.BUFFER_SIZE:
                return received_data

    def accept(self):
        obj, address = socket.socket.accept(self)
        obj.__class__ = MPSocket
        return obj, address

