import random
from primes_numbers import primes_numbers
from math import gcd


class ElGamal:

    def __init__(self, __public_key=None, __private_key=None):
        self.private_key = __private_key  # pgx
        self.public_key = __public_key  # pgy

    @property
    def private_key(self):
        return self._private_key

    @private_key.setter
    def private_key(self, value):
        if value is None:
            self._private_key = self.make_private_key()
        else:
            self._private_key = value

    @property
    def public_key(self):
        return self._public_key

    @public_key.setter
    def public_key(self, value):
        if value is None:
            self._public_key = self.make_public_key(self._private_key)
        else:
            self._public_key = value

    @classmethod
    def set_keys(cls, public_key, private_key):
        return cls(public_key, private_key)

    @staticmethod
    def xgcd(a, b):
        x, old_x = 0, 1
        y, old_y = 1, 0
        while b != 0:
            quotient = a // b
            a, b = b, a - quotient * b
            old_x, x = x, old_x - quotient * x
            old_y, y = y, old_y - quotient * y
        return a, old_x, old_y

    @staticmethod
    def find_primitive_root(p):
        p1 = 2
        p2 = (p - 1) // p1
        while True:
            g = random.randint(2, p - 1)
            if not pow(g, (p - 1) // p1, p) == 1:
                if not pow(g, (p - 1) // p2, p) == 1:
                    return g

    def create_k(self):
        k = random.randint(2, self.private_key[0] - 2)
        while gcd(self.private_key[0] - 1, k) != 1:
            k = random.randint(1, self.private_key[0] - 2)

        return k

    def make_public_key(self, pgx):
        p, g, x = pgx
        y = pow(g, x, p)
        return p, g, y

    def make_private_key(self):
        p = primes_numbers.generate_prime_numbers(33)  # generate p
        g = self.find_primitive_root(p)
        x = random.randint(2, p - 2)
        return p, g, x

    def make_sign(self, message, module=None, k=None):
        if module is None:
            module = self.private_key[0] - 1
        if k is None:
            k = self.create_k()

        int_m = message
        p, g, x = self.private_key
        # k = find_k(p,module)
        r = pow(g, k, p)
        gcd_a, inverted_k, b_coeff = self.xgcd(k, module)
        s = ((int_m - x * r) * inverted_k) % module

        return r, s

    def verify_sign(self, message, sign):
        p, g, y = self.public_key
        r, s = sign
        if (not (0 < r < p)) and (not (0 < s < p - 1)):
            # print("Invalid parameters")
            return False, "Invalid parameters"

        int_m = message

        if (pow(y, r, p) * pow(r, s, p)) % p == pow(g, int_m, p):
            # print("Verified")
            return True, "Verified"
        else:
            # print("Not verified")
            return False, "Not verified"
