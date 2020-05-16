import socket

from .client_socket import *


class ServerSocket:

    def __init__(self, port):
        self.port = port

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(("", self.port))
        self.s.listen(1)

    def __del__(self):
        self.close()

    def wait_for_client(self):
        return ClientSocket(self.s.accept()[0])

    def close(self):
        self.s.close()
