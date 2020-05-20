# because i want to call python server_main.py directly
import sys
import RSA
import os.path
from send_recv_file import *

sys.path.append("..")

from sockets_classes.server_socket import *


DESTINATION = 'server_recv'


def get_ip_address():
    """Вернуть IP-адрес компьютера.

    Фиктивное UDP-подключение к google's DNS,
    после подключения getsockname() вернет локальный IP.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


if __name__ == "__main__":
    server_socket = ServerSocket(0)

    print("Порт (ID): {}".format(server_socket.s.getsockname()[1]))

    client_socket = server_socket.wait_for_client()

    # AUTH
    RSA.auth_init(server_socket.s.getsockname()[1], public_key_A, client_socket, '[A -> B]')

    RSA.auth_recv(private_key_B, client_socket, 'A')

    try:
        while True:
            if not recv_file(client_socket, DESTINATION):
                break

            print('File arrived')

            while True:
                file_name = input('Enter file name or "quit" to quit: ')

                if file_name == 'quit':
                    break
                elif not os.path.exists(file_name):
                    print('Invalid file name, try again...')
                    continue
                else:
                    break

            if file_name == 'quit':
                break

            print('File sent')

            send_file(file_name, client_socket)
    except AttributeError:
        pass

    client_socket.close()
    server_socket.close()
