

class Message(object):

    TYPE_PING = 'ping'
    TYPE_TIMEOUT = 'timeout'
    TYPE_DISCONNECT = 'disconnect'
    TYPE_GAMEDATA = 'gamedata'

    def __init__(self, message=None):
        self.type = None
        self.timestamp = None
        self.data = None
        pass

    def __repr__(self):
        pass

    def get_type(self):
        return self.type

    def set_type(self, type):
        pass

    def get_data(self):
        return self.data

    def set_data(self, data):
        pass

    def get_timestamp(self):
        return self.timestamp

    def set_timestamp(self, timestamp):
        pass