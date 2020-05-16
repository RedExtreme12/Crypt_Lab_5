"""Cript-functions."""

from math import sqrt, gcd
from random import randrange, getrandbits


def miller_rabin_on_base_2(n: int) -> bool:
    d = n - 1
    s = 0

    while d % 2 == 0:
        d = d // 2
        s += 1

    x = pow(2, d, n)

    if x == 1 or x == n - 1:
        return True
    for i in range(s - 1):
        x = pow(x, 2, n)

        if x == 1:
            return False
        elif x == n - 1:
            return True

    return False


def subs_generate(k, n, U, V, P, Q, D):
    # k, n, U, V, P, Q, D = map(int, (k, n, U, V, P, Q, D))
    binary = list(map(int, str(bin(k))[2:]))
    Q = int(Q)

    number_of_subscript = 1

    for bit in binary[1:]:
        U = U * V % n
        V = (pow(V, 2, n) - 2 * pow(Q, number_of_subscript, n))
        number_of_subscript *= 2

        # Идём от младшего к старшему биту, пропуская первый бит, если бит == 1, то с помощью формул сложения,
        # вычисляем U(2k+1), V(2k+1).
        if bit == 1:

            # Рассматриваем 3 три случая:
            # P * U + V делится на 2,
            # D * U + P * V делится на 2,
            # оба не делятся на 2
            if (P * U + V) % 2 == 0:
                if (D * U + P * V) % 2 == 0:
                    U, V = (P * U + V) // 2, (D * U + P * V) // 2
                else:
                    # Если D * U + P * V не делится на 2, мы добавляем к этому числу n.
                    # n - нечётное число, нечётное + нечётное = чётное => мы можем делить на 2.
                    U, V = (P * U + V) // 2, (D * U + P * V + n) // 2
            elif (D * U + P * V) % 2 == 0:
                U, V = (P * U + V + n) // 2, (D * U + P * V) // 2
            else:
                U, V = (P * U + V + n) // 2, (D * U + P * V + n) // 2

            number_of_subscript += 1
            U, V = U % n, V % n

    return U, V


def lucas(n, D, P, Q) -> bool:
    U, V = subs_generate(n + 1, n, 1, P, P, Q, D)
    # k, n, U, V, P, Q, D

    if U == 0 or V == 0:
        return True

    d = n + 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for r in range(s):
        V = (pow(V, 2, n) - 2 * pow(Q, d * (2 ** r), n)) % n
        if V == 0:
            return True

    return False


def jacobi(a, n) -> int:
    j = 1

    while a:
        while a % 2 == 0:
            a = a // 2

            if n % 8 == 3 or n % 8 == 5:
                j = -j

        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            j = -j
        a = a % n

    if n == 1:
        return j
    else:
        return 0


def D_chooser(candidate) -> int:
    D = 5
    while jacobi(D, candidate) != -1:
        D += 2 if D > 0 else -2  # 5, -7, 9, -11, 13...
        D *= -1
    return D


def baillie_psw(candidate) -> bool:
    # Проверка на тривиальные делители (меньше 50), на составных числах это ускорит работу.
    for known_prime in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
        if candidate == known_prime:
            return True
        elif candidate % known_prime == 0:
            return False

    if not miller_rabin_on_base_2(candidate):
        return False

    # Число не должно быть полным квадратом, иначе параметры Селфриджа будут вычислены неправильно.
    if sqrt(int(candidate + 0.5)) ** 2 == candidate:
        return False

    D = D_chooser(candidate)
    if not lucas(candidate, D, 1, (1 - D) / 4):  # Q = (1 - D) / 4
        return False

    return True


def generate_prime_candidate(length: int) -> int:
    """ Генерация псевдослучайных (нечётных) чисел
    """
    p = getrandbits(length)
    # Устанавливаем MSB и LSB В 1.
    p |= (1 << length - 1) | 1
    return p


def generate_prime_numbers(length: int):
    candidate = generate_prime_candidate(length)

    while not baillie_psw(candidate):
        candidate = generate_prime_candidate(length)
    return candidate
