import sys
import RSA
import os.path
from send_recv_file import *

sys.path.append("..")

from sockets_classes.server_socket import *

server_host = '192.168.1.8'  # HOST ADDRESS

DESTINATION = 'client_recv'


if __name__ == "__main__":
    port = int(input("Enter ID: "))  # ID!!!!

    client_socket = ClientSocket.connect_to_server(server_host, port)

    # AUTH
    RSA.auth_recv(private_key_A, client_socket, 'B')

    RSA.auth_init(port, public_key_B, client_socket, '[B -> A]')

    try:
        while True:
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

            send_file(file_name, client_socket)

            print('File sent')

            if not recv_file(client_socket, DESTINATION):
                break

            print('File arrived')
    except AttributeError:
        pass

    client_socket.close()
