import json


class Message(object):

    TYPE_PING = 'ping'
    TYPE_TIMEOUT = 'timeout'
    TYPE_DISCONNECT = 'disconnect'
    TYPE_GAMEDATA = 'gamedata'

    def __init__(self, msg=None):
        if msg:
            try:
                message = json.loads(msg)
                self.type = message["type"]
                self.timestamp = message["timestamp"]
                self.data = message["data"]
                return
            except:
                pass

        self.client = None
        self.type = None
        self.timestamp = None
        self.data = None

    def __repr__(self):
        msg = {
            "type": self.type,
            "timestamp": self.timestamp,
            "data": self.data
        }
        return json.dumps(msg)

    def get_type(self):
        return self.type

    def set_type(self, type):
        self.type = type

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

    def get_timestamp(self):
        return self.timestamp

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp
