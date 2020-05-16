import hashlib
from ElGamal import ElGamal


public_key_A = (417850465, 3482499239)
private_key_A = (1399167937, 3482499239)

public_key_B = (350152603, 2155636267)
private_key_B = (104492947, 2155636267)

BLOCK_SIZE = 65536

ELGamal_private_key = (8425670959, 6625693567, 1413249786)
ELGamal_public_key = (8425670959, 6625693567, 6942823274)


def get_file_hash(f_name) -> int:
    file_hash = hashlib.sha256()

    with open(f_name, 'rb') as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = f.read(BLOCK_SIZE)

    hash_sum = int(file_hash.hexdigest(), 16)

    return hash_sum


def send_file(f_name, c_socket):
    with open(f_name, 'r') as f:
        file_content = f.read()

    signature = ElGamal.set_keys(ELGamal_public_key, ELGamal_private_key)

    _hash = get_file_hash(f_name)

    sign = signature.make_sign(_hash)

    # parse
    c_socket.send_string(str(sign[0]) + '-' + str(sign[1]) + '-' + str(_hash))

    c_socket.send_string(f_name)
    c_socket.send_string(file_content)


def recv_file(c_socket, dest):
    sign = c_socket.recv_string().split('-')
    r = int(sign[0])
    s = int(sign[1])
    _hash = int(sign[2])

    signature = ElGamal.set_keys(ELGamal_public_key, ELGamal_private_key)
    signature.verify_sign(_hash, (r, s))

    file_name = c_socket.recv_string()
    message = c_socket.recv_string()

    with open(f'{dest}/{file_name}', 'w') as f:
        f.write(message)

    return message
