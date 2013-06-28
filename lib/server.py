import select
import socket
import sys
from lib.utl import net


class Server:

    def __init__(self, port):
        """
        port -- int
        """
        self.host = ''
        self.port = port
        self.backlog = 5
        self.size = 8192
        self.inp = []
        self.out = []
        self.err = []
        self.data = {}

    def listen(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(self.backlog)
        self.inp = [self.server]
        print "Started server on port %d..." % self.port

    def receive(self):
        self.data = {k: {} for k in self.data.keys()}  # clear data values
        timeout = 0.02  # seconds
        inp, out, err = select.select(self.inp, self.out, self.err, timeout)
        for s in inp:
            if s == self.server:
                client, address = self.server.accept()
                self.inp.append(client)
            else:
                data = s.recv(self.size)
                if data:
                    self.data[s] = net.net_eval(data)
                else:
                    s.close()
                    self.inp.remove(s)

    def send(self):
        for s in self.data.keys():
            s.send(net.net_repr(self.data[s]))

    def close(self):
        self.server.close()

    def get_data(self):
        """
        Returns dict
        """
        return self.data

    def set_data(self, data):
        """
        data -- dict
        """
        self.data = data
