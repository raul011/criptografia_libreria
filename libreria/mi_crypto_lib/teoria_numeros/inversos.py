"""
inversos.py — Inversos multiplicativos modulares
=================================================

Métodos implementados:
    1. Usando el Teorema de Euler: a^{φ(n)−1} mod n
    2. Usando el Algoritmo de Euclides Extendido
    3. Por búsqueda exhaustiva (didáctico)
"""

from math import gcd


def mcd(a, b):
    """
    Calcula el Máximo Común Divisor usando el algoritmo de Euclides.

    Ejemplo
    -------
    >>> mcd(12, 8)
    4
    >>> mcd(17, 5)
    1
    """
    while b:
        a, b = b, a % b
    return a


def euclides_extendido(a, b):
    """
    Algoritmo de Euclides Extendido.

    Encuentra x, y tales que: a·x + b·y = mcd(a, b)

    Retorna
    -------
    tuple (mcd, x, y)

    Ejemplo
    -------
    >>> euclides_extendido(35, 15)
    (5, 1, -2)
    """
    if a == 0:
        return b, 0, 1

    g, x1, y1 = euclides_extendido(b % a, a)
    x = y1 - (b // a) * x1
    y = x1

    return g, x, y


def inverso_extendido(a, n):
    """
    Calcula el inverso multiplicativo de a módulo n usando
    el Algoritmo de Euclides Extendido.

    Parámetros
    ----------
    a : int
        Número cuyo inverso se busca.
    n : int
        Módulo.

    Retorna
    -------
    int
        Inverso multiplicativo a⁻¹ tal que (a · a⁻¹) ≡ 1 (mod n).

    Raises
    ------
    ValueError
        Si mcd(a, n) ≠ 1 (no existe inverso).

    Ejemplo
    -------
    >>> inverso_extendido(3, 26)
    9
    >>> (3 * 9) % 26
    1
    """
    g, x, _ = euclides_extendido(a % n, n)
    if g != 1:
        raise ValueError(
            f"No existe inverso multiplicativo de {a} módulo {n} "
            f"(mcd = {g})"
        )
    return x % n


def inverso_euler(a, n):
    """
    Calcula el inverso multiplicativo de a módulo n usando
    el Teorema de Euler:  a⁻¹ ≡ a^{φ(n)−1} (mod n)

    Requiere que mcd(a, n) = 1.

    Parámetros
    ----------
    a : int
        Número cuyo inverso se busca.
    n : int
        Módulo.

    Retorna
    -------
    int
        Inverso multiplicativo.

    Ejemplo
    -------
    >>> inverso_euler(3, 26)
    9
    """
    if gcd(a, n) != 1:
        raise ValueError(
            f"No existe inverso multiplicativo de {a} módulo {n} "
            f"(no son coprimos)"
        )

    # Importación local para evitar dependencia circular
    from .phi import phi

    phi_n = phi(n)
    return pow(a, phi_n - 1, n)


def inverso_fuerza_bruta(a, n):
    """
    Encuentra el inverso multiplicativo por búsqueda exhaustiva.

    Útil para verificación y fines didácticos.

    Ejemplo
    -------
    >>> inverso_fuerza_bruta(3, 26)
    9
    """
    a = a % n
    for x in range(1, n):
        if (a * x) % n == 1:
            return x

    raise ValueError(
        f"No existe inverso multiplicativo de {a} módulo {n}"
    )


def tabla_inversos(n):
    """
    Genera una tabla con todos los inversos multiplicativos módulo n.

    Retorna
    -------
    dict[int, int]
        Diccionario {a: a⁻¹} para cada a coprimo con n.

    Ejemplo
    -------
    >>> tabla_inversos(10)
    {1: 1, 3: 7, 7: 3, 9: 9}
    """
    tabla = {}
    for a in range(1, n):
        if gcd(a, n) == 1:
            tabla[a] = inverso_extendido(a, n)
    return tabla
