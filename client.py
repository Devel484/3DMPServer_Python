import mpsocket


class Client(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = mpsocket.MPSocket(mpsocket.socket.AF_INET, mpsocket.socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.ip, self.port))

    def send(self, msg: str):
        self.socket.sendall(bytes(msg.encode("utf-8")))

if __name__ == "__main__":
    client = Client("10.42.0.232", 11111)
    client.connect()
    client.send("Hallo Christoph")