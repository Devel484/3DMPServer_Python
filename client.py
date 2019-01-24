from socket import socket, AF_INET, SOCK_STREAM
from message import Message
from threading import Thread
import time


class Client(Thread):

    def __init__(self, ip, port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.start()

    def connect(self, nickname):
        self.socket.connect((self.ip, self.port))

        message = Message()
        message.set_type(Message.TYPE_CONNECT)
        message.set_timestamp(int(time.time()*1000))
        message.set_data({"nickname": nickname})
        client.send(message)

    def send(self, msg):
        self.socket.sendall(bytes((str(msg)+'\0').encode("utf-8")))

    def on_message(self, msg):
        """
        This event is called if a new message was received.
        :param msg: Message (hopefully in JSON-format as string)
        :type msg: str
        :return: None
        """
        message = Message(msg)
        print(message)

    def run(self):
        """
        This functions starts a loop which checks if data was received and append data pieces together til a full
        message was transmitted.
        :return: None
        """
        received_data = ""
        while True:
            piece = str(self.socket.recv(4096).decode("utf-8"))
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


if __name__ == "__main__":
    client = Client("192.168.137.154", 11111)
    client.connect("Devel484")

