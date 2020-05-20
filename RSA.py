import logging.config
import random
from math import gcd

from hash_function import utils
from primes_numbers import primes_numbers
from sockets_classes.server_socket import *

COUNT_BYTES = 2048
KEY = 0x133457799BBCDFF1  # Hash-function.

HASH_R_B_LENGTH = 20
ID_LENGTH = 5

logging.config.fileConfig('Configs/logging_RSA.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def is_prime(x):
    if x == 2:
        return True
    if x < 2 or x % 2 == 0:
        return False
    for n in range(3, int(x ** 0.5) + 2, 2):
        if x % n == 0:
            return False
    return True


def multiplicative_inverse(e, phi):
    """
    Euclid's extended algorithm for finding the multiplicative inverse of two numbers
    """
    d, next_d, temp_phi = 0, 1, phi
    while e > 0:
        quotient = temp_phi // e
        d, next_d = next_d, d - quotient * next_d
        temp_phi, e = e, temp_phi - quotient * e
    if temp_phi > 1:
        raise ValueError('e is not invertible by modulo phi.')
    if d < 0:
        d += phi
    return d


def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime!')
    elif p == q:
        raise ValueError('P and Q cannot be equal!')
    n = p * q
    e = 0
    phi = (p - 1) * (q - 1)
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)
    d = multiplicative_inverse(e, phi)
    return (e, n), (d, n)


def encrypt_by_symbol(message,public_key):
    (e,n) = public_key
    return [(ord(ch)**e)%n for ch in message]


def decrypt_by_symbol(message,private_key):
    (d,n) = private_key
    return "".join([chr((ch**d)%n) for ch in message])


def encrypt(num, public_key):
    (e,n) = public_key
    return pow(num,e,n)


def decrypt(num, private_key):
    (d, n) = private_key
    return pow(num, d, n)


def string_to_bits(_str):
    return "".join((bin(ord(c))[2:]).zfill(8) for c in _str)


def string_from_bits(bin_str):
    return "".join(chr(int(bin_str[i:i+8],2)) for i in range(0, len(bin_str)-7, 8))


def encrypt_str(message, public_key):
    (e, n) = public_key
    res = ""
    bin_str = string_to_bits(message)
    bin_str += "1"
    while len(bin_str) % (n.bit_length()-1) != 0:
        bin_str += "0"
    for i in range(0, len(bin_str), n.bit_length()-1):
        enc_i = pow(int(bin_str[i:i+n.bit_length()-1], 2), e, n)
        bin_i = format(enc_i, 'b').zfill(n.bit_length())
        res += bin_i
    return res


def decrypt_str(message, private_key):
    (d, n) = private_key
    bin_str = ""
    for i in range(0,len(message), n.bit_length()):
        num = int(message[i:i+n.bit_length()], 2)
        dec_num = pow(num, d, n)
        bin_str += format(dec_num, 'b').zfill(n.bit_length() - 1)
    return string_from_bits(bin_str[:bin_str.rfind("1")])


# FROM CLIENT B
def auth_init(ID, public_key_A, sock, sides):
    R_B = primes_numbers.generate_prime_numbers(16)  # ~ 5 chars

    hash_R_B = str(utils.encrypt(R_B, KEY))  # ~ 19 chars

    while len(hash_R_B) < HASH_R_B_LENGTH:
        hash_R_B += '0'

    enc = hash_R_B + str(ID) + encrypt_str(str(R_B) + str(ID), public_key_A)

    sock.send_string(enc)  # B to A

    if sock.recv_string() == str(R_B):
        logger.info(f'Authentication success {sides}')
    else:
        logger.info(f'Authentication failed')


def auth_recv(private_key_A, client_socket, side):
    enc = client_socket.recv_string()
    key = enc[HASH_R_B_LENGTH + ID_LENGTH:]

    decr = decrypt_str(key, private_key_A)[:-5]  # R_B
    client_socket.send_string(decr)

    logging.info(f'Side {side} proves')  # {sides}


# НЕ ТОТ ПРОТОКОЛ


def authenticate_from_me(sock: socket):
    p = primes_numbers.generate_prime_numbers(10)
    q = primes_numbers.generate_prime_numbers(10)

    while p == q:
        p = primes_numbers.generate_prime_numbers(10)
        q = primes_numbers.generate_prime_numbers(10)

    en, dn = generate_keypair(p, q)

    e = en[0]
    n = en[0]
    d = dn[0]

    _en = str(e) + ' ' + str(n)

    sock.send(_en.encode())

    r = int(sock.recv(COUNT_BYTES).decode())
    _k = (r ** d) % n  # k'

    sock.send(str(_k).encode())

    result = bool(sock.recv(COUNT_BYTES).decode())  # if success, we get 1.

    return result


def authenticate(sock: socket):
    en = sock.recv(COUNT_BYTES).decode().split(' ')
    e, n = int(en[0]), int(en[1])

    k = random.randint(1, n - 1)

    r = (k ** e) % n

    sock.send(str(r).encode())

    _k = int(sock.recv(COUNT_BYTES).decode())

    if k == _k:
        sock.send(str(True).encode())  # Было str(1)
    else:
        sock.send(str(False).encode())
