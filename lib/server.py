import select
import socket
import sys
from lib.utl import net


class Server(object):

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
        self.attempts = {}
        self.timeout = 0.02  # seconds

    def listen(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(self.backlog)
        self.inp = [self.server]
        print "Started server on port %d..." % self.port

    def receive(self):
        self.data = {k: {} for k in self.data.keys()}  # clear data values
        inp, out, err = select.select(self.inp, self.out,
                                      self.err, self.timeout)
        for s in inp:
            if s == self.server:
                client, address = self.server.accept()
                self.inp.append(client)
            else:
                try:
                    data = s.recv(self.size)
                    if data:
                        self.data[s] = net.net_eval(data)
                except socket.error:
                    # Do nothing if can not receive, see send()
                    pass

    def send(self):
        for s in self.data.keys():
            try:
                s.send(net.net_repr(self.data[s]))
            except socket.error:
                if s not in self.attempts:
                    print "Client cowardly disconnected, retrying..."
                    self.attempts[s] = 1
                else:
                    self.attempts[s] += 1
                    if self.attempts[s] > (1.0 / self.timeout) * 10:
                        print "Client cowardly disconnected, stopping retries."
                        del self.data[s]
                        s.close()
                        self.inp.remove(s)

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
