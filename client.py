import mpsocket


class Client(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = mpsocket.MPSocket(mpsocket.socket.AF_INET, mpsocket.socket.SOCK_STREAM)