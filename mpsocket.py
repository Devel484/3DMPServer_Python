import socket


class MPSocket(socket.socket):

    BUFFER_SIZE = 4096

    @staticmethod
    def receive(conn):
        received_data = ""
        while True:
            piece = str(conn.recv(MPSocket.BUFFER_SIZE))
            find = piece.find("\\x00")
            if find != -1:
                received_data += piece[:find]
                on_message(received_data)
                received_data = piece[find:]
            else:
                received_data += piece
            #if len(piece) < MPSocket.BUFFER_SIZE:
                #return received_data
