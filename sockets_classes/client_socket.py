import socket
import struct


class ClientSocket:

    def __init__(self, s):
        self.s = s

    def __del__(self):
        self.close()

    @classmethod
    def connect_to_server(cls, server_host, server_port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server_host, server_port))

        return cls(s)

    def recvall(self, n):
        data = b""
        while len(data) < n:
            packet = self.s.recv(n - len(data))
            if not packet:
                return None

            data += packet

        return data

    def send_bytes_msg(self, bytes_msg):
        bytes_msg = struct.pack(">I", len(bytes_msg)) + bytes_msg  # > stands for BigEndian, I - for unsigned int
        self.s.sendall(bytes_msg)

    def recv_bytes_msg(self):
        raw_msglen = self.recvall(4)

        if not raw_msglen:
            return None

        msglen = struct.unpack(">I", raw_msglen)[0]

        return self.recvall(msglen)

    def send_int(self, i):
        self.send_bytes_msg(struct.pack(">i", i))

    def recv_int(self):
        i = self.recv_bytes_msg()

        return None if i is None else struct.unpack(">i", i)[0]

    def send_float(self, f):
        self.send_bytes_msg(struct.pack(">f", f))

    def recv_float(self):
        f = self.recv_bytes_msg()

        return None if f is None else struct.unpack(">f", f)[0]

    def send_string(self, s):
        self.send_bytes_msg(s.encode("UTF-8"))

    def recv_string(self):
        s = self.recv_bytes_msg()

        return None if s is None else s.decode("UTF-8")

    def close(self):
        self.s.close()
