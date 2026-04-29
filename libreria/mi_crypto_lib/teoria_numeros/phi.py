"""
phi.py — Cálculo de la función indicatriz de Euler φ(n)
========================================================

Implementa múltiples formas de calcular φ(n):
    1. Método directo (contando coprimos)
    2. Mediante factorización en primos
    3. Para el caso especial n = p·q (usado en RSA)
"""

from math import gcd


def factorizar(n):
    """
    Descompone n en sus factores primos.

    Retorna un diccionario {primo: exponente}.

    Ejemplo
    -------
    >>> factorizar(12)
    {2: 2, 3: 1}
    >>> factorizar(60)
    {2: 2, 3: 1, 5: 1}
    """
    if n < 2:
        return {}

    factores = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factores[d] = factores.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factores[n] = factores.get(n, 0) + 1

    return factores


def phi(n):
    """
    Calcula la función indicatriz de Euler φ(n).

    Utiliza la fórmula basada en factorización:
        φ(n) = n · ∏(1 − 1/p) para cada primo p que divide a n

    Parámetros
    ----------
    n : int
        Número entero positivo.

    Retorna
    -------
    int
        Valor de φ(n).

    Ejemplo
    -------
    >>> phi(1)
    1
    >>> phi(10)
    4
    >>> phi(36)
    12
    """
    if n < 1:
        raise ValueError("n debe ser un entero positivo")
    if n == 1:
        return 1

    resultado = n
    factores = factorizar(n)

    for p in factores:
        resultado -= resultado // p

    return resultado


def phi_directo(n):
    """
    Calcula φ(n) de forma directa contando cuántos enteros en [1, n)
    son coprimos con n.

    Útil para verificación y fines didácticos.

    Ejemplo
    -------
    >>> phi_directo(10)
    4
    """
    if n < 1:
        raise ValueError("n debe ser un entero positivo")
    if n == 1:
        return 1

    return sum(1 for k in range(1, n) if gcd(k, n) == 1)


def phi_pq(p, q):
    """
    Calcula φ(n) para el caso especial n = p·q donde p y q son primos.

    Fórmula: φ(p·q) = (p − 1)(q − 1)

    Este caso es fundamental en RSA.

    Parámetros
    ----------
    p : int
        Primer número primo.
    q : int
        Segundo número primo.

    Retorna
    -------
    int
        Valor de φ(p·q).

    Ejemplo
    -------
    >>> phi_pq(5, 7)
    24
    >>> phi_pq(11, 13)
    120
    """
    return (p - 1) * (q - 1)
