from socket import socket, AF_INET, SOCK_STREAM
from message import Message
import time
import json

class Client(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = socket(AF_INET, SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.ip, self.port))

    def send(self, msg):
        self.socket.sendall(bytes((str(msg)+'\0').encode("utf-8")))

if __name__ == "__main__":
    client = Client("192.168.137.154", 11111)
    client.connect()

    message = Message()
    message.set_client("Username")
    message.set_type(Message.TYPE_PING)
    message.set_timestamp(int(time.time()*1000))
    message.set_data({"ping": True})

    client.send(message)
