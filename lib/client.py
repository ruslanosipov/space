import socket
from lib.utl import net
import sys


class Client:

    def __init__(self, host, port):
        """
        host -- str
        port -- int
        """
        self.host = host
        self.port = port
        self.size = 8192
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
            sys.exit("Can not receive, server has been disconnected")
        return net.net_eval(data)

    def send(self, data):
        """
        data -- dict
        """
        sent = self.socket.send(net.net_repr(data))
        if not sent:
            sys.exit("Can not send, server has been disconnected")
