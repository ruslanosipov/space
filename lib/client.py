import socket


class Client:
    def __init__(self, host, port):
        """
        host -- str
        port -- int
        """
        self.host = host
        self.port = port
        self.size = 4096
        self.connect()

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def receive(self):
        """
        Returns dict
        """
        data = self.socket.recv(self.size)
        if not data:
            raise RuntimeError("Can not receive, socket connection broken!")
        return eval(data)

    def send(self, data):
        """
        data -- dict
        """
        sent = self.socket.send(repr(data))
        if not sent:
            raise RuntimeError("Can not send, socket connection broken!")
