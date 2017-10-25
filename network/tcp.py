import socket as sock
import threading

class TcpConnection(object):
    """
    Transport layer protocol
    """

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

    def client_connect(self):
        client = client, address = self.socket.accept()
        return client
     
    def connect(self):
        self.socket.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print("'Serving '{0}:{1}' ...".format(self.host, self.port))
        self.listen()

    def recieve_4096(user):
        return client.recv(4096)

    def recv_256(self):
        return self.socket.recv(256)

    def send(self, data):
        try:
            self.client.send(data)
        except BrokenPipeError:
            pass
