from threading import Thread


class UserInterface(Thread):
    """
    ClientConnection represents a socket connection to one client/player
    """

    def __init__(self, server):
        """
        Creates a instance of UserInterface which handles all input on console.
        """
        Thread.__init__(self)
        self.server = server
        print("Interface active.")
        self.start()

    def run(self):
        while not self.server.EXIT:
            command = input('Awaiting command...\n')
            if command == "shutdown":
                print("Shutdown server...")
                self.server.shutdown()
            elif command == "show clients":
                print("Active clients:")
                client_dict = self.server.get_client_dict()
                for nickname, client_connection in client_dict.items():
                    print("%s -> %s" % (client_connection.client_socket.getpeername(), nickname))
            else:
                print("Unknown command.")
