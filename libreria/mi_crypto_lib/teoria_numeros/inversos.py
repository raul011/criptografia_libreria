"""
Inversos multiplicativos modulo n.
Dos metodos:
  1. Teorema de Euler: a^phi(n)-1 mod n
  2. Euclides extendido: ax + ny = mcd(a,n)
"""

from .funciones_matematicas.phi import phi
from .funciones_matematicas.mcd import mcd


def inverso_multiplicativo(a, n):
    """
    Calcula el inverso usando el Algoritmo de Euclides Extendido.
    Retorna diccionario con resultado o error.
    """
    if mcd(a, n) != 1:
        return {"error": str(a) + " y " + str(n) + " no son coprimos, no existe inverso"}

    gcd, x, y = _euclides_extendido(a, n)
    inverso = x % n

    return {
        "a": a,
        "n": n,
        "inverso": inverso,
        "verificacion": (a * inverso) % n == 1
    }


def _euclides_extendido(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = _euclides_extendido(b, a % b)
    return gcd, y1, x1 - (a // b) * y1


def inverso_euler(a, n):
    """
    Calcula el inverso usando el Teorema de Euler:
        a^(-1) = a^(phi(n)-1) mod n
    """
    if mcd(a, n) != 1:
        return {"error": str(a) + " y " + str(n) + " no son coprimos"}

    phi_n = phi(n)
    inverso = pow(a, phi_n - 1, n)

    return {
        "a": a,
        "n": n,
        "phi_n": phi_n,
        "inverso": inverso,
        "formula": "a^-1 = a^(phi(n)-1) mod n = " + str(a) + "^(" + str(phi_n) + "-1) mod " + str(n),
        "verificacion": (a * inverso) % n == 1
    }
