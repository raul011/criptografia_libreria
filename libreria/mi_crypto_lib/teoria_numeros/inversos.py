"""
Inversos multiplicativos módulo n.
Implementa el Teorema de Euler y el Algoritmo de Euclides Extendido.
"""

from .phi import phi


def mcd(a, b):
    """Calcula el máximo común divisor."""
    while b:
        a, b = b, a % b
    return a


def son_coprimos(a, b):
    """Verifica si a y b son coprimos."""
    return mcd(a, b) == 1


def inverso_euler(a, n):
    """
    Calcula el inverso multiplicativo de 'a' módulo 'n'
    usando el Teorema de Euler: a^(phi(n)-1) mod n.
    """
    if not son_coprimos(a, n):
        raise ValueError(str(a) + " y " + str(n) + " no son coprimos")

    phi_n = phi(n)
    return pow(a, phi_n - 1, n)


def inverso_extendido(a, n):
    """
    Calcula el inverso multiplicativo de 'a' módulo 'n'
    usando el Algoritmo de Euclides Extendido.
    """
    if not son_coprimos(a, n):
        raise ValueError(str(a) + " y " + str(n) + " no son coprimos")

    def _euclides(a, b):
        if b == 0:
            return a, 1, 0
        gcd, x1, y1 = _euclides(b, a % b)
        return gcd, y1, x1 - (a // b) * y1

    _, x, _ = _euclides(a, n)
    return x % n
