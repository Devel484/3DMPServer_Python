from message import Message, UnknownMessageTypeException, WrongJSONFormatException, ConnectingException
from threading import Thread
from socket import timeout
import time


class ClientConnection(Thread):
    """
    ClientConnection represents a socket connection to one client/player
    """

    # == INFO ==
    # message   : Class message
    # msg       : Received Data

    STATUS_CONNECTING = "connecting"
    STATUS_IN_LOBBY = "in_lobby"
    STATUS_READY = "ready"
    STATUS_IN_GAME = "in_game"

    def __init__(self, server, client_socket):
        """
        Creates a instance of ClientConnection with a reference to the server and the client socket.
        :param server: Server
        :type server: Server
        :param client_socket: Socket of the client
        :type client_socket: socket
        """
        Thread.__init__(self)
        self.server = server
        self.client_socket = client_socket
        self.nickname = None
        self.last_timestamp = None
        self.error_count = 0
        self.stop = False
        self.status = self.STATUS_CONNECTING
        self.start()

    def send_message(self, message):
        """
        Send a message over a socket to the client. The message is UTF-8 encoded and a binary zero is appended to
        ensure the split between multiple messages.
        :param message: Message to be send
        :type message: Message
        :return: None
        """
        print("[OUT] %s" % message)
        self.client_socket.sendall(bytes((str(message)+'\0').encode("utf-8")))

    def on_message(self, msg):
        """
        This event is called if a new message was received.
        :param msg: Message (hopefully in JSON-format as string)
        :type msg: str
        :return: None
        """
        try:
            message = Message(msg, self)
            print("[IN]  %s" % message)
            msg_type = message.get_type()

            # Check for msg_type
            if self.nickname is None and msg_type == message.TYPE_CONNECT:
                self.on_connect(message.get_data())
            elif self.nickname is None and msg_type != message.TYPE_CONNECT:
                raise ConnectingException("connecting not yet completed")
            elif self.nickname is not None and msg_type == message.TYPE_CONNECT:
                raise ConnectingException("connecting already completed")
            else:
                if msg_type == message.TYPE_CONNECT:
                    self.on_connect(message.get_data())
                elif msg_type == message.TYPE_DISCONNECT:
                    self.on_disconnect("client")
                elif msg_type == message.TYPE_PING:
                    self.on_ping()
                elif msg_type == message.TYPE_TIMEOUT:
                    self.on_timeout()
                elif msg_type == message.TYPE_GAMEDATA:
                    self.on_gamedata(message)
                else:
                    raise UnknownMessageTypeException("unknown type of message")
        except UnknownMessageTypeException as e:
            self.on_error(e)
        except WrongJSONFormatException as e:
            self.on_error(e)
        except ConnectingException as e:
            self.on_error(e)
        else:
            self.error_count = 0

    def on_connect(self, data):
        """
        This event is called if a connection message was received.
        :param data: data of message
        :type data: str
        :return: None
        """
        try:
            nickname = data["nickname"]
            if not self.server.on_connect(self, nickname):
                raise ConnectingException("change nickname")

            # Send timeout information
            self.nickname = nickname
            message = Message()
            message.set_type(Message.TYPE_CONNECT)
            message.set_data({"timeout": self.server.CLIENT_TIMEOUT})
            self.send_message(message)

        except ConnectingException as e:
            self.on_error(e)

    def on_disconnect(self, reason):
        """
        This event is called if a disconnect message was received. The socket will be closed and a event another event
        on the server will be called.
        :param reason: Reason for disconnecting
        :type reason: String
        :return: None
        """
        # Close connection
        self.stop = True
        self.server.on_disconnect(self, reason)

    def on_ping(self):
        """
        This event is called if a ping message was received. A pong message will be send instant.
        :return: None
        """
        # Create and send pong message
        message = Message()
        message.set_type(message.TYPE_PONG)
        self.send_message(message)

    def on_timeout(self):
        """
        This event will be called if a timeout happens.
        :return: None
        """
        pass

    def on_gamedata(self, message):
        """
        This event will be called if game date was received.
        :return: None
        """
        timestamp = message.get_timestamp()
        # Accept gamedata message only if it's a new one
        if timestamp > self.last_timestamp:
            self.last_timestamp = timestamp
            self.server.on_gamedata(message)

    def on_error(self, exception):
        """
        This event will be called if a error happens.
        :param exception: Raised Exception
        :type exception: Exception
        :return: None
        """
        if self.error_count <= 3:
            message = Message()
            message.set_type(message.TYPE_ERROR)
            message.set_data({"error": exception.args[0]})
            self.send_message(message)
            self.error_count += 1
        else:
            self.on_disconnect("to many errors")

    def set_nickname(self, nickname):
        self.nickname = nickname

    def get_nickname(self):
        return self.nickname

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def run(self):
        """
        This functions starts a loop which checks if data was received and append data pieces together til a full
        message was transmitted.
        :return: None
        """
        received_data = ""
        while not self.server.EXIT and not self.stop:
            try:
                self.client_socket.settimeout(0.2)
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

            except timeout:
                pass
