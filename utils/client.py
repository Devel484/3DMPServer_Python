from socket import socket, AF_INET, SOCK_STREAM, timeout
from utils.message import Message
from threading import Thread
import time


class Client(Thread):

    def __init__(self, ip, port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.last_ping = None
        self.timeout = None

    def connect(self, nickname):
        self.socket.connect((self.ip, self.port))
        self.start()
        message = Message()
        message.set_type(Message.TYPE_CONNECT)
        message.set_timestamp(int(time.time()*1000))
        message.set_data({"nickname": nickname})
        client.send(message)

    def send(self, msg):
        print("[OUT]"+str(msg))
        self.socket.sendall(bytes((str(msg)+'\0').encode("utf-8")))

    def on_message(self, msg):
        """
        This event is called if a new message was received.
        :param msg: Message (hopefully in JSON-format as string)
        :type msg: str
        :return: None
        """
        message = Message(msg)
        print("[IN]"+str(message))

        if message.get_type() == Message.TYPE_ERROR:
            return self.on_error(message)

        if message.get_type() == Message.TYPE_CONNECT:
            return self.on_connect(message)

    def on_error(self, message):
        pass

    def on_connect(self, message):
        data = message.get_data()
        if "timeout" not in data:
            return

        self.timeout = data["timeout"]
        self.send_ping()

    def on_tick(self):
        if not self.timeout:
            return

        if not self.last_ping:
            return

        current_time = time.time()
        spread = current_time - self.last_ping
        if spread > self.timeout/2:
            self.send_ping()

    def send_ping(self):
        message = Message()
        message.set_type(Message.TYPE_PING)
        message.set_timestamp(int(time.time()*1000))
        message.set_data({"pong": True})
        self.last_ping = time.time()
        client.send(message)

    def run(self):
        """
        This functions starts a loop which checks if data was received and append data pieces together til a full
        message was transmitted.
        :return: None
        """
        received_data = ""
        while True:
            self.on_tick()
            try:
                self.socket.settimeout(0.2)
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
            except timeout:
                pass


if __name__ == "__main__":
    client = Client("127.0.0.1", 11111)
    client.connect("Devel484")
